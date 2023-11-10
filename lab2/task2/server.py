import socket
import struct

# Predefined DNS records
DNS_RECORDS = {
    'google.com': ['192.165.1.1', '192.165.1.10'],
    'youtube.com': ['192.165.1.2'],
    'uwaterloo.ca': ['192.165.1.3'],
    'wikipedia.org': ['192.165.1.4'],
    'amazon.ca': ['192.165.1.5'],
}

def parse_domain_name(query):
    domain_name = ''
    length = query[12]
    position = 13
    while length != 0:
        domain_name += query[position:position+length].decode('utf-8') + '.'
        position += length + 1
        length = query[position - 1]
    return domain_name[:-1]  # Remove the trailing dot

# Function to create DNS response
def create_dns_response(query, domain_name):
    transaction_id = query[:2]
    flags = b'\x81\x80'
    questions = query[4:6]
    answer_rrs = struct.pack('>H', len(DNS_RECORDS[domain_name]))
    authority_rrs = b'\x00\x00'
    additional_rrs = b'\x00\x00'
    answer = b''

    for ip in DNS_RECORDS[domain_name]:
        record = b'\xc0\x0c'  # Name pointer to domain name in the query
        record += b'\x00\x01'  # Type A
        record += b'\x00\x01'  # Class IN
        record += struct.pack('>I', 260)  # TTL
        record += b'\x00\x04'  # Length of the IP address
        record += socket.inet_aton(ip)  # IP address
        answer += record

    return transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + answer

# Function to display data in Hex format
def display_hex(data):
    return ' '.join(f'{b:02x}' for b in data)

# Main server function
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('127.0.0.1', 10053))
    print("DNS Server is running on 127.0.0.1:10053")

    while True:
        query, client_address = server_socket.recvfrom(512)
        print("Request from:", client_address)
        print("Request (in Hex):", display_hex(query))

        domain_name = parse_domain_name(query)

        if domain_name in DNS_RECORDS:
            response = create_dns_response(query, domain_name)
            server_socket.sendto(response, client_address)
            print("Response (in Hex):", display_hex(response))
        else:
            print(f"Domain name not found: {domain_name}")

if __name__ == '__main__':
    main()
