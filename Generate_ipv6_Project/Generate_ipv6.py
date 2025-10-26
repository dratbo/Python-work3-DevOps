import sys
import ipaddress
import re


def parse_fqdn(fqdn):
    match = re.match(r'(?:super-cluster|contest)-(\d+)-(\d+)\.kit\.yandex\.net', fqdn)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None


def generate_ipv6(cluster_num, node_num, ipv4):
    cluster_hex = format(cluster_num, 'x')
    node_hex = format(node_num, 'x')

    ipv6_str = f"2b4e:{cluster_hex}:{node_hex}::{ipv4}"

    ipv6_obj = ipaddress.IPv6Address(ipv6_str)

    return str(ipv6_obj)


def main():
    try:
        with open('input.txt', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = sys.stdin.readlines()

    records = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) < 5:
            continue

        fqdn = parts[0]
        record_type = parts[3]
        address = parts[4]

        if address == "None":
            continue

        cluster_num, node_num = parse_fqdn(fqdn)
        if cluster_num is None or node_num is None:
            continue

        key = (cluster_num, node_num)

        if key not in records:
            records[key] = {'A': None, 'AAAA': None}

        if record_type == 'A':
            records[key]['A'] = address
        elif record_type == 'AAAA':
            records[key]['AAAA'] = address

    results = []

    for (cluster_num, node_num), record in records.items():
        if record['A']:
            expected_ipv6 = generate_ipv6(cluster_num, node_num, record['A'])

            if record['AAAA'] != expected_ipv6:
                results.append((cluster_num, node_num, expected_ipv6))

    results.sort(key=lambda x: (x[0], x[1]))

    for cluster_num, node_num, ipv6 in results:
        print(f"{cluster_num} {node_num} {ipv6}")


if __name__ == "__main__":
    main()