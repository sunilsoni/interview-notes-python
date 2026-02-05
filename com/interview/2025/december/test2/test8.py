#!/usr/bin/env python3
"""
AWS CloudFormation OO API Generator
====================================

WHAT THIS SCRIPT DOES:
----------------------
1. Downloads AWS CloudFormation API specification (ZIP file) from AWS CloudFront
2. Extracts JSON specification files from the ZIP
3. Parses the JSON to understand AWS resource structures
4. Generates Python dataclass files from those structures

FLOW DIAGRAM:
-------------
    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
    │   Download   │ --> │   Extract    │ --> │    Parse     │ --> │   Generate   │
    │   ZIP File   │     │    JSON      │     │    Spec      │     │  Dataclasses │
    └──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘

DIRECTORY STRUCTURE CREATED:
----------------------------
    script_location/
    └── edo-challenge/
        ├── specs/
        │   ├── CloudFormationResourceSpecification.zip
        │   └── specs/
        │       └── *.json files (extracted)
        └── oo/
            └── generated_*.py files (output)

USAGE:
------
    python aws_cf_generator.py <service_name_spec>

    Example:
        python aws_cf_generator.py AWS_Lambda_Function
        python aws_cf_generator.py AWS_S3_Bucket

EXAMPLE OUTPUT (generated dataclass):
-------------------------------------
    from dataclasses import dataclass

    @dataclass
    class S3Bucket:
        \"\"\"https://docs.aws.amazon.com/...\"\"\"
        BucketName: str
        AccessControl: str = None
        Tags: list = None

REQUIREMENTS:
-------------
    pip install requests

AUTHOR NOTES:
-------------
    - This script converts AWS CloudFormation resource specifications to Python dataclasses
    - Dataclasses provide a clean, type-hinted way to represent AWS resources
    - The generated code can be used for infrastructure-as-code tooling
"""

# =============================================================================
# IMPORTS
# =============================================================================

import io  # For file I/O type hints (used in type annotations)
from pathlib import Path  # Modern, object-oriented file path handling
from argparse import ArgumentParser, RawTextHelpFormatter  # Command-line argument parsing
from zipfile import ZipFile  # For extracting ZIP archives
import json  # For parsing JSON specification files
import os  # For file/directory operations
import sys  # For system-specific parameters and exit

# Third-party import - needs: pip install requests
try:
    import requests  # HTTP library for downloading files
except ImportError:
    print("ERROR: 'requests' library not installed!")
    print("Please run: pip install requests")
    sys.exit(1)

# =============================================================================
# CONFIGURATION CONSTANTS
# =============================================================================

# URL to AWS's CloudFormation specification file
# NOTE: Original had typo (.zi instead of .zip) - FIXED HERE
CF_API_SPEC_URL = "https://d1uauaxba7bl26.cloudfront.net/latest/CloudFormationResourceSpecification.zip"

# Alternative URLs if the above doesn't work:
# CF_API_SPEC_URL = "https://d33vqc0rt9ld30.cloudfront.net/latest/gzip/CloudFormationResourceSpecification.json"

# -----------------------------------------------------------------------------
# Directory Configuration
# -----------------------------------------------------------------------------
# Path(__file__) = Path to this script file
# .parent = Directory containing this script
# / "edo-challenge" = Subdirectory named "edo-challenge"

EDO_DIR = Path(__file__).parent / "edo-challenge"  # Base output directory
SPEC_DIR = EDO_DIR / "specs"  # Where downloaded/extracted specs go
OO_DIR = EDO_DIR / "oo"  # Where generated Python files go
ZIPFNAME = SPEC_DIR / "CloudFormationResourceSpecification.zip"  # Downloaded ZIP filename

# -----------------------------------------------------------------------------
# Processing Constants
# -----------------------------------------------------------------------------

# Download chunk size: 1MB (1024 * 1024 bytes)
# Using chunks prevents loading entire file into memory at once
# This is important for large files (the spec can be 50MB+)
CHUNK_SIZE_IN_BYTES = 1048576  # 1 MB

# Header line for all generated Python modules
# This imports the dataclass decorator which we use for all generated classes
MODULE_IMPORT = "from dataclasses import dataclass"

# Lambda function used to sort properties by their "Required" field
# tup[0] = property name (string)
# tup[1] = property data (dict containing "Required": True/False)
# This sorts so Required=True comes first (important for dataclass field ordering)
SORTER = lambda tup: tup[1].get("Required", False)


# =============================================================================
# TYPE CONVERSION FUNCTION
# =============================================================================

def get_type(type_: str) -> str:
    """
    Convert AWS CloudFormation type names to Python type names.

    AWS CloudFormation uses its own type naming convention in the spec.
    This function maps those to standard Python type annotations.

    MAPPING TABLE:
    ┌─────────────────┬───────────────┐
    │ AWS Type        │ Python Type   │
    ├─────────────────┼───────────────┤
    │ String          │ str           │
    │ Integer         │ int           │
    │ Boolean         │ bool          │
    │ Double          │ float         │
    │ Json            │ dict          │
    │ Timestamp       │ str           │
    │ Long            │ float         │
    │ Map             │ dict          │
    │ List            │ list          │
    │ (unknown)       │ (unchanged)   │
    └─────────────────┴───────────────┘

    Parameters:
    -----------
    type_ : str
        The AWS type name from the CloudFormation spec
        (underscore suffix to avoid shadowing built-in 'type')

    Returns:
    --------
    str
        The corresponding Python type name

    Examples:
    ---------
    >>> get_type("String")
    'str'
    >>> get_type("Integer")
    'int'
    >>> get_type("CustomType")  # Unknown type returned as-is
    'CustomType'
    """
    # Dictionary mapping AWS types to Python types
    type_mapping = {
        "String": "str",  # Text data
        "Integer": "int",  # Whole numbers
        "Boolean": "bool",  # True/False values
        "Double": "float",  # Decimal numbers (double precision)
        "Json": "dict",  # JSON objects map to Python dictionaries
        "Timestamp": "str",  # Timestamps stored as ISO format strings
        "Long": "float",  # Large numbers (Python handles this as float)
        "Map": "dict",  # Key-value mappings
        "List": "list",  # Arrays/sequences
    }

    # .get(type_, type_) means:
    # - If type_ is in the dict, return mapped value
    # - If type_ is NOT in the dict, return type_ unchanged (default)
    return type_mapping.get(type_, type_)


# =============================================================================
# DOWNLOAD FUNCTION
# =============================================================================

def download_aws_cf_api_spec() -> bool:
    """
    Download the AWS CloudFormation API specification ZIP file.

    This function:
    1. Makes an HTTP GET request to AWS CloudFront CDN
    2. Streams the response in chunks (memory efficient)
    3. Writes chunks to a local ZIP file

    WHY STREAMING?
    --------------
    Without streaming:              With streaming:
    ┌─────────────────────┐        ┌─────────────────────┐
    │ Load ENTIRE file    │        │ Load 1MB chunk      │
    │ into memory first   │        │ Write to disk       │
    │ (could be 50MB+)    │        │ Repeat...           │
    │ Then write to disk  │        │ (constant ~1MB RAM) │
    └─────────────────────┘        └─────────────────────┘

    Returns:
    --------
    bool
        True if download successful, False otherwise

    Raises:
    -------
    Does not raise - catches exceptions and returns False
    """
    print(f"[DOWNLOAD] Starting download from: {CF_API_SPEC_URL}")
    print(f"[DOWNLOAD] Saving to: {ZIPFNAME}")

    try:
        # Using context managers (with statements) for automatic cleanup
        # - open(..., "wb") = Open file for Writing in Binary mode
        # - requests.get(..., stream=True) = Don't download all at once

        with open(ZIPFNAME, "wb") as zipf:
            with requests.get(CF_API_SPEC_URL, stream=True, timeout=60) as transfer:

                # raise_for_status() raises an HTTPError if status code is 4xx or 5xx
                # Examples: 404 Not Found, 500 Internal Server Error
                transfer.raise_for_status()

                # Get total file size for progress indication (if available)
                total_size = int(transfer.headers.get('content-length', 0))
                downloaded = 0

                # iter_content() yields chunks of the response body
                # This is the key to memory-efficient downloading
                for chunk in transfer.iter_content(chunk_size=CHUNK_SIZE_IN_BYTES):
                    if chunk:  # Filter out keep-alive chunks
                        zipf.write(chunk)
                        downloaded += len(chunk)

                        # Print progress
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r[DOWNLOAD] Progress: {percent:.1f}% ({downloaded}/{total_size} bytes)", end="")

                print()  # New line after progress

        print(f"[DOWNLOAD] Successfully downloaded {downloaded} bytes")
        return True

    except requests.exceptions.RequestException as e:
        # Catches all requests-related errors:
        # - ConnectionError: Network problems
        # - Timeout: Request took too long
        # - HTTPError: Bad HTTP response
        print(f"[DOWNLOAD] ERROR: Failed to download - {e}")
        return False
    except IOError as e:
        # Catches file writing errors
        print(f"[DOWNLOAD] ERROR: Failed to write file - {e}")
        return False


# =============================================================================
# EXTRACTION FUNCTION
# =============================================================================

def extract_json() -> bool:
    """
    Extract the downloaded ZIP file containing JSON specifications.

    The ZIP file contains multiple JSON files, each describing
    different AWS services and their CloudFormation resources.

    Directory structure after extraction:
    -------------------------------------
    specs/
    ├── CloudFormationResourceSpecification.zip (the ZIP file)
    └── specs/
        ├── AWS_Lambda_Function.json
        ├── AWS_S3_Bucket.json
        ├── AWS_EC2_Instance.json
        └── ... (many more)

    Returns:
    --------
    bool
        True if extraction successful, False otherwise
    """
    print(f"[EXTRACT] Extracting: {ZIPFNAME}")
    print(f"[EXTRACT] Target directory: {SPEC_DIR}")

    try:
        # ZipFile context manager ensures proper file handling
        with ZipFile(ZIPFNAME, 'r') as zipf:
            # List contents for debugging
            file_list = zipf.namelist()
            print(f"[EXTRACT] Found {len(file_list)} files in archive")

            # Show first few files
            for fname in file_list[:5]:
                print(f"[EXTRACT]   - {fname}")
            if len(file_list) > 5:
                print(f"[EXTRACT]   ... and {len(file_list) - 5} more")

            # Extract all files to SPEC_DIR
            zipf.extractall(SPEC_DIR)

        print(f"[EXTRACT] Successfully extracted all files")
        return True

    except FileNotFoundError:
        print(f"[EXTRACT] ERROR: ZIP file not found at {ZIPFNAME}")
        return False
    except Exception as e:
        print(f"[EXTRACT] ERROR: Failed to extract - {e}")
        return False


# =============================================================================
# AWS API SPECIFICATION PARSER CLASS
# =============================================================================

class AWSAPISpecParser:
    """
    Parse AWS CloudFormation specification files and generate Python dataclasses.

    This class:
    1. Loads a JSON specification file for a specific AWS service
    2. Parses the ResourceType and PropertyTypes sections
    3. Generates a Python module with dataclass definitions

    CLOUDFORMATION SPEC STRUCTURE:
    ------------------------------
    {
        "ResourceType": {
            "AWS::S3::Bucket": {
                "Documentation": "https://docs...",
                "Properties": {
                    "BucketName": {
                        "Required": true,
                        "PrimitiveType": "String",
                        "Documentation": "..."
                    },
                    "Tags": {
                        "Required": false,
                        "Type": "List",
                        "Documentation": "..."
                    }
                }
            }
        },
        "PropertyTypes": {
            "AWS::S3::Bucket.CorsConfiguration": {
                "Documentation": "...",
                "Properties": { ... }
            }
        }
    }

    GENERATED OUTPUT:
    -----------------
    from dataclasses import dataclass

    @dataclass
    class CorsConfiguration:
        \"\"\"https://docs...\"\"\"
        CorsRules: list

    @dataclass
    class S3Bucket:
        \"\"\"https://docs...\"\"\"
        BucketName: str
        Tags: list = None

    Attributes:
    -----------
    spec : dict
        The loaded JSON specification
    spec_path : str
        Path to the loaded specification file

    DATACLASS FIELD ORDERING RULES:
    -------------------------------
    In Python dataclasses, fields with default values MUST come AFTER
    fields without default values:

        @dataclass
        class Example:
            required_field: str          # No default - must be first
            optional_field: str = None   # Has default - must be last

    This is why we sort properties by "Required" field (Required=True first).
    """

    # Template string for generating dataclass definitions
    # {class_name} and {docstring} are replaced using .format()
    class_template = """
@dataclass
class {class_name}:
    {docstring}
"""

    def __init__(self, spec_path: str):
        """
        Initialize parser with a specification file path.

        Parameters:
        -----------
        spec_path : str
            Name of the spec file (without .json extension)
            Example: "AWS_Lambda_Function"
        """
        self.spec_path = spec_path
        self.spec = self.load_spec(spec_path)
        print(f"[PARSER] Initialized parser for: {spec_path}")

    def load_spec(self, service_name_spec: str) -> dict:
        """
        Load and parse a JSON specification file.

        Parameters:
        -----------
        service_name_spec : str
            Name of the service spec file (without .json extension)

        Returns:
        --------
        dict
            Parsed JSON specification

        File path constructed:
            SPEC_DIR / "specs" / "{service_name_spec}.json"
            Example: edo-challenge/specs/specs/AWS_Lambda_Function.json
        """
        # Construct full path to JSON file
        spec_file = SPEC_DIR / "specs" / f"{service_name_spec}.json"
        print(f"[PARSER] Loading spec file: {spec_file}")

        try:
            with open(spec_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"[PARSER] Successfully loaded specification")
            return data
        except FileNotFoundError:
            print(f"[PARSER] ERROR: Spec file not found: {spec_file}")
            # List available spec files
            self._list_available_specs()
            raise
        except json.JSONDecodeError as e:
            print(f"[PARSER] ERROR: Invalid JSON in spec file: {e}")
            raise

    def _list_available_specs(self) -> None:
        """Helper method to list available specification files."""
        specs_dir = SPEC_DIR / "specs"
        if specs_dir.exists():
            print("[PARSER] Available specification files:")
            for f in sorted(specs_dir.glob("*.json"))[:20]:
                print(f"[PARSER]   - {f.stem}")
            json_files = list(specs_dir.glob("*.json"))
            if len(json_files) > 20:
                print(f"[PARSER]   ... and {len(json_files) - 20} more")

    def get_module_name(self) -> str:
        """
        Generate Python module filename from resource type.

        TRANSFORMATION:
        ---------------
        Input:  "AWS::Lambda::Function"

        Step 1: .replace("::", "_")
                "AWS_Lambda_Function"

        Step 2: .replace("AWS_", "")
                "Lambda_Function"

        Step 3: .casefold()  (lowercase)
                "lambda_function"

        Step 4: + ".py"
                "lambda_function.py"

        Returns:
        --------
        str
            Python module filename (e.g., "lambda_function.py")
        """
        # Get the first (usually only) resource type key
        # ResourceType dict typically has one entry like "AWS::S3::Bucket"
        resource_type_key = list(self.spec.get("ResourceType", {}).keys())[0]

        # Transform to valid Python module name
        module_name = (
                resource_type_key
                .replace("::", "_")  # AWS::Lambda::Function → AWS_Lambda_Function
                .replace("AWS_", "")  # AWS_Lambda_Function → Lambda_Function
                .casefold()  # Lambda_Function → lambda_function (lowercase)
                + ".py"  # lambda_function → lambda_function.py
        )

        print(f"[PARSER] Generated module name: {module_name}")
        return module_name

    @staticmethod
    def _get_item_type(prop_data: dict) -> str:
        """
        Determine the Python type for a property.

        AWS specs have two ways to specify types:
        1. "PrimitiveType": For basic types (String, Integer, etc.)
        2. "Type": For complex types (List, Map, custom types)

        DECISION FLOW:
        --------------
                    prop_data
                        │
                        ▼
            ┌─── Has "PrimitiveType"? ───┐
            │                            │
           Yes                          No
            │                            │
            ▼                            ▼
        Return converted            Return converted
        primitive type              complex type

        Parameters:
        -----------
        prop_data : dict
            Property definition from the spec containing type information

        Returns:
        --------
        str
            Python type name

        Examples:
        ---------
        >>> _get_item_type({"PrimitiveType": "String"})
        'str'
        >>> _get_item_type({"Type": "List"})
        'list'
        """
        # Check for primitive type first (takes precedence)
        if "PrimitiveType" in prop_data:
            return get_type(prop_data["PrimitiveType"])

        # Fall back to complex type
        if "Type" in prop_data:
            return get_type(prop_data["Type"])

        # Default if neither is present
        return "Any"

    def _get_member(self, prop_name: str, prop_data: dict) -> str:
        """
        Generate a dataclass member/field definition string.

        Parameters:
        -----------
        prop_name : str
            Name of the property (e.g., "BucketName")
        prop_data : dict
            Property definition containing type and required info

        Returns:
        --------
        str
            Formatted member string for the dataclass

        OUTPUT FORMAT:
        --------------
        Required property:
            "    BucketName: str"

        Optional property (Required=False):
            "    Tags: list = None"

        WHY DEFAULT = None FOR OPTIONAL?
        ---------------------------------
        - Makes the field truly optional when instantiating the dataclass
        - Follows Python convention for optional parameters
        - None is a safe default that indicates "not provided"
        """
        # Get the Python type for this property
        python_type = self._get_item_type(prop_data)

        # Build base member string with 4-space indentation
        member = f"    {prop_name}: {python_type}"

        # Add default value for optional (non-required) properties
        # prop_data.get("Required", False) - default to False if key missing
        is_required = prop_data.get("Required", False)

        if is_required:
            return member  # No default value
        else:
            return member + " = None"  # Add default value

    def _write_property_types(self, f: io.TextIOWrapper) -> None:
        """
        Write PropertyTypes as dataclasses to the output file.

        PropertyTypes are helper/nested types used by the main resource.
        For example, AWS::S3::Bucket has PropertyTypes like:
        - CorsConfiguration
        - LifecycleConfiguration
        - WebsiteConfiguration

        Parameters:
        -----------
        f : io.TextIOWrapper
            Open file handle to write to

        SORTING EXPLANATION:
        --------------------
        Properties are sorted by "Required" field in DESCENDING order
        (reverse=True means True comes before False)

        This ensures required fields come first in the dataclass,
        which is mandatory in Python dataclasses.

        Before sorting: [("Tags", Required=False), ("Name", Required=True)]
        After sorting:  [("Name", Required=True), ("Tags", Required=False)]
        """
        print(f"[PARSER] Writing PropertyTypes...")

        property_types = self.spec.get("PropertyTypes", {})

        if not property_types:
            print(f"[PARSER]   No PropertyTypes found")
            return

        for key, data in property_types.items():
            # Skip "Tag" type - it's a common type defined elsewhere
            if key == "Tag":
                print(f"[PARSER]   Skipping common type: Tag")
                continue

            # Extract class name from key
            # Key format: "AWS::S3::Bucket.CorsConfiguration"
            # We want: "CorsConfiguration"
            if "." in key:
                class_name = key.split(".")[1]
            else:
                class_name = key.replace("::", "")

            print(f"[PARSER]   Writing PropertyType: {class_name}")

            # Create docstring from documentation URL
            doc_url = data.get("Documentation", "No documentation available")
            docstring = f'"""{doc_url}"""'

            # Write class header using template
            f.write(self.class_template.format(
                class_name=class_name,
                docstring=docstring
            ))

            # Get and sort properties
            properties = data.get("Properties", {})

            # Sort by Required field, descending (Required=True first)
            sorted_properties = sorted(
                properties.items(),
                key=SORTER,
                reverse=True  # True > False, so required fields come first
            )

            # Write each member
            for prop_name, prop_data in sorted_properties:
                member = self._get_member(prop_name, prop_data)
                f.write(member + "\n")

        print(f"[PARSER]   Wrote {len(property_types)} PropertyTypes")

    def _write_resource_type(self, f: io.TextIOWrapper) -> None:
        """
        Write the main ResourceType as a dataclass to the output file.

        ResourceType is the primary AWS resource being defined.
        For example: AWS::S3::Bucket, AWS::Lambda::Function

        Parameters:
        -----------
        f : io.TextIOWrapper
            Open file handle to write to

        NOTE ON ORIGINAL BUG:
        ---------------------
        The original code had "PProperties" which was a typo.
        It should be "Properties" - FIXED in this version.

        SORTING:
        --------
        Same as PropertyTypes - required fields must come first
        in dataclass definitions.
        """
        print(f"[PARSER] Writing ResourceType...")

        resource_types = self.spec.get("ResourceType", {})

        if not resource_types:
            print(f"[PARSER]   No ResourceType found")
            return

        for key, data in resource_types.items():
            # Transform class name
            # "AWS::S3::Bucket" → "S3Bucket"
            class_name = key.replace("::", "").replace("AWS", "")

            print(f"[PARSER]   Writing ResourceType: {class_name}")

            # Create docstring
            doc_url = data.get("Documentation", "No documentation available")
            docstring = f'"""{doc_url}"""'

            # Write class header
            f.write(self.class_template.format(
                class_name=class_name,
                docstring=docstring
            ))

            # Get properties - NOTE: Original had typo "PProperties", fixed to "Properties"
            properties = data.get("Properties", {})

            # Sort by Required field, descending (Required=True first)
            sorted_properties = sorted(
                properties.items(),
                key=SORTER,
                reverse=True  # Required fields first
            )

            # Write each member
            for prop_name, prop_data in sorted_properties:
                member = self._get_member(prop_name, prop_data)
                f.write(member + "\n")

        print(f"[PARSER]   Wrote {len(resource_types)} ResourceTypes")

    def create_module(self) -> Path:
        """
        Create the complete Python module with all dataclasses.

        This is the main entry point that orchestrates:
        1. Creating/opening the output file
        2. Writing the import statement
        3. Writing PropertyTypes (helper classes)
        4. Writing ResourceType (main class)

        Returns:
        --------
        Path
            Path to the created Python module

        OUTPUT FILE STRUCTURE:
        ----------------------
        from dataclasses import dataclass

        @dataclass
        class HelperType1:
            ...

        @dataclass
        class HelperType2:
            ...

        @dataclass
        class MainResourceType:
            ...
        """
        # Determine output file path
        output_path = OO_DIR / self.get_module_name()
        print(f"[PARSER] Creating module: {output_path}")

        try:
            # Open file for writing (creates if doesn't exist, overwrites if does)
            with open(output_path, "w", encoding='utf-8') as f:
                # Write header comment
                f.write(f"# Auto-generated from AWS CloudFormation specification\n")
                f.write(f"# Source: {self.spec_path}\n")
                f.write(f"# Do not edit manually\n\n")

                # Write import statement
                f.write(MODULE_IMPORT + "\n")

                # Write Optional import for type hints (useful for None defaults)
                f.write("from typing import Optional, List, Dict, Any\n")

                # Write PropertyTypes (helper/nested types)
                self._write_property_types(f)

                # Write ResourceType (main resource)
                self._write_resource_type(f)

            print(f"[PARSER] Successfully created module: {output_path}")
            return output_path

        except IOError as e:
            print(f"[PARSER] ERROR: Failed to write module - {e}")
            raise


# =============================================================================
# DIRECTORY SETUP FUNCTION
# =============================================================================

def setup_directories() -> bool:
    """
    Create necessary directory structure.

    Creates:
    --------
    edo-challenge/
    ├── specs/    (for downloaded/extracted specification files)
    └── oo/       (for generated Python modules)

    Returns:
    --------
    bool
        True if all directories created/exist, False on error

    MKDIR PARAMETERS:
    -----------------
    - parents=True: Create parent directories if they don't exist
    - exist_ok=True: Don't raise error if directory already exists
    """
    print("[SETUP] Creating directory structure...")

    try:
        # Create each directory
        # parents=True allows creating nested directories
        # exist_ok=True prevents error if already exists

        EDO_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[SETUP]   Created/verified: {EDO_DIR}")

        SPEC_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[SETUP]   Created/verified: {SPEC_DIR}")

        OO_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[SETUP]   Created/verified: {OO_DIR}")

        print("[SETUP] Directory structure ready")
        return True

    except PermissionError as e:
        print(f"[SETUP] ERROR: Permission denied - {e}")
        return False
    except Exception as e:
        print(f"[SETUP] ERROR: Failed to create directories - {e}")
        return False


# =============================================================================
# DEMO MODE FUNCTION (when no spec file exists)
# =============================================================================

def create_demo_spec() -> str:
    """
    Create a demo specification file for testing when AWS download fails.

    This creates a minimal but valid CloudFormation spec JSON file
    that can be used to test the generator without internet access.

    Returns:
    --------
    str
        Name of the created demo spec file (without .json extension)
    """
    print("[DEMO] Creating demo specification file...")

    # Demo spec mimicking AWS::S3::Bucket structure
    demo_spec = {
        "ResourceType": {
            "AWS::S3::Bucket": {
                "Documentation": "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-bucket.html",
                "Properties": {
                    "BucketName": {
                        "Documentation": "The name of the bucket.",
                        "Required": False,
                        "PrimitiveType": "String"
                    },
                    "AccessControl": {
                        "Documentation": "Access control for the bucket.",
                        "Required": False,
                        "PrimitiveType": "String"
                    },
                    "Tags": {
                        "Documentation": "Tags for the bucket.",
                        "Required": False,
                        "Type": "List"
                    },
                    "VersioningConfiguration": {
                        "Documentation": "Versioning configuration.",
                        "Required": False,
                        "Type": "VersioningConfiguration"
                    }
                }
            }
        },
        "PropertyTypes": {
            "AWS::S3::Bucket.VersioningConfiguration": {
                "Documentation": "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-versioningconfig.html",
                "Properties": {
                    "Status": {
                        "Documentation": "Versioning status.",
                        "Required": True,
                        "PrimitiveType": "String"
                    }
                }
            },
            "AWS::S3::Bucket.CorsConfiguration": {
                "Documentation": "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors.html",
                "Properties": {
                    "CorsRules": {
                        "Documentation": "CORS rules.",
                        "Required": True,
                        "Type": "List"
                    }
                }
            }
        }
    }

    # Create the nested specs directory
    demo_specs_dir = SPEC_DIR / "specs"
    demo_specs_dir.mkdir(parents=True, exist_ok=True)

    # Write the demo spec file
    demo_file = demo_specs_dir / "AWS_S3_Bucket_Demo.json"
    with open(demo_file, 'w', encoding='utf-8') as f:
        json.dump(demo_spec, f, indent=2)

    print(f"[DEMO] Created demo spec: {demo_file}")
    return "AWS_S3_Bucket_Demo"


# =============================================================================
# MAIN FUNCTION
# =============================================================================

def main():
    """
    Main entry point for the AWS CloudFormation OO API Generator.

    WORKFLOW:
    ---------
    1. Parse command-line arguments
    2. Create directory structure
    3. Download AWS CloudFormation spec (or use demo)
    4. Extract JSON files from ZIP
    5. Parse specification and generate Python dataclasses
    6. Output success message with file path

    COMMAND LINE USAGE:
    -------------------
    python script.py <service_name_spec>
    python script.py --demo
    python script.py --list

    Examples:
        python script.py AWS_Lambda_Function
        python script.py AWS_S3_Bucket
        python script.py --demo
    """

    # -------------------------------------------------------------------------
    # ARGUMENT PARSING
    # -------------------------------------------------------------------------

    # Create argument parser with formatted description
    parser = ArgumentParser(
        description=__doc__,  # Use module docstring as description
        formatter_class=RawTextHelpFormatter  # Preserve formatting in help text
    )

    # Add arguments
    parser.add_argument(
        "service_name_spec",
        type=str,
        nargs='?',  # Makes it optional
        default=None,
        help="Name of the AWS service spec file (e.g., AWS_Lambda_Function)"
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run with demo data (no download required)"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List available specification files"
    )

    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip downloading (use existing files)"
    )

    # Parse arguments
    args = parser.parse_args()

    # -------------------------------------------------------------------------
    # BANNER
    # -------------------------------------------------------------------------

    print("=" * 70)
    print("AWS CloudFormation OO API Generator")
    print("=" * 70)
    print()

    # -------------------------------------------------------------------------
    # DIRECTORY SETUP
    # -------------------------------------------------------------------------

    if not setup_directories():
        print("\n[ERROR] Failed to create directories. Exiting.")
        sys.exit(1)

    print()

    # -------------------------------------------------------------------------
    # DEMO MODE
    # -------------------------------------------------------------------------

    if args.demo:
        print("[MODE] Running in DEMO mode")
        service_name_spec = create_demo_spec()

    # -------------------------------------------------------------------------
    # LIST MODE
    # -------------------------------------------------------------------------

    elif args.list:
        print("[MODE] Listing available specifications")
        specs_dir = SPEC_DIR / "specs"
        if specs_dir.exists():
            print("\nAvailable specification files:")
            for f in sorted(specs_dir.glob("*.json")):
                print(f"  - {f.stem}")
        else:
            print("\nNo specifications found. Run with a service name first to download.")
        sys.exit(0)

    # -------------------------------------------------------------------------
    # NORMAL MODE
    # -------------------------------------------------------------------------

    else:
        # Check if service name was provided
        if args.service_name_spec is None:
            print("[ERROR] No service name provided!")
            print("\nUsage:")
            print("  python script.py <service_name_spec>")
            print("  python script.py --demo")
            print("  python script.py --list")
            print("\nExamples:")
            print("  python script.py AWS_Lambda_Function")
            print("  python script.py AWS_S3_Bucket")
            sys.exit(1)

        service_name_spec = args.service_name_spec

        # ---------------------------------------------------------------------
        # DOWNLOAD
        # ---------------------------------------------------------------------

        if not args.skip_download:
            print()
            if not download_aws_cf_api_spec():
                print("\n[WARNING] Download failed. Trying demo mode...")
                service_name_spec = create_demo_spec()
            else:
                # -----------------------------------------------------------------
                # EXTRACTION
                # -----------------------------------------------------------------
                print()
                if not extract_json():
                    print("\n[ERROR] Extraction failed. Exiting.")
                    sys.exit(1)
        else:
            print("[SKIP] Skipping download (--skip-download flag)")

    # -------------------------------------------------------------------------
    # PARSING AND GENERATION
    # -------------------------------------------------------------------------

    print()
    print(f"[MAIN] Processing service: {service_name_spec}")

    try:
        # Create parser and generate module
        parser_obj = AWSAPISpecParser(service_name_spec)
        output_path = parser_obj.create_module()

        # Success message
        print()
        print("=" * 70)
        print("SUCCESS!")
        print("=" * 70)
        print(f"Generated dataclass module: {output_path}")
        print()
        print("You can now import the generated classes:")
        print(f"  from edo-challenge.oo.{output_path.stem} import *")
        print()

    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        print("\nTip: Try running with --demo flag to test with sample data:")
        print("  python script.py --demo")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# =============================================================================
# SCRIPT ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    """
    This block only executes when the script is run directly,
    not when it's imported as a module.

    Example:
        python aws_cf_generator.py AWS_Lambda_Function  # __name__ == "__main__"

        import aws_cf_generator  # __name__ == "aws_cf_generator"
    """
    main()