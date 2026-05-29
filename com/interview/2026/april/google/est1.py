import re


def parse_wrapped_output(raw_text):
    # Regex to find the local (EthX/Y) and remote (EthA/B) interfaces
    pattern = re.compile(r'(?P<local>Eth\d+(?:/\d+)*)\s+.*?(?P<remote>Eth\d+(?:/\d+)*)')

    lines = [line.strip() for line in raw_text.strip().splitlines() if line.strip()]
    pairs = {}

    i = 0
    while i < len(lines):
        current_line = lines[i]
        match = pattern.search(current_line)

        if match:
            # Found everything on one line
            pairs[match.group('local')] = match.group('remote')
        elif i + 1 < len(lines):
            # It's a wrapped line! Combine the device name line with the next line
            combined_line = current_line + " " + lines[i + 1]
            combined_match = pattern.search(combined_line)

            if combined_match:
                pairs[combined_match.group('local')] = combined_match.group('remote')
                # Skip the next line since we just consumed it
                i += 1

        i += 1

    return pairs