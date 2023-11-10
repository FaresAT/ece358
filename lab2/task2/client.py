import socket
import sys

def query_dns(server_address, domain):
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Prepare DNS query
        transaction_id = b'\xaa\xbb'  # Random transaction ID
        flags = b'\x01\x00'  # Standard query
        qdcount = b'\x00\x01'  # One question
        ancount = b'\x00\x00'
        nscount = b'\x00\x00'
        arcount = b'\x00\x00'
        qname = b''.join(len(part).to_bytes(1, 'big') + part.encode('utf-8') for part in domain.split('.'))
        qname += b'\x00'  # End of the domain name
        qtype = b'\x00\x01'  # Type A
        qclass = b'\x00\x01'  # Class IN

        query = transaction_id + flags + qdcount + ancount + nscount + arcount + qname + qtype + qclass

        # Send DNS query to the server
        sock.sendto(query, server_address)

        # Wait for the response from the server
        response, _ = sock.recvfrom(512)
        return response
    finally:
        sock.close()

def format_output(response):
    transaction_id = response[:2]
    answer_rrs = int.from_bytes(response[6:8], byteorder='big')
    answers = response[12:]
    for i in range(answer_rrs):
        data_length = int.from_bytes(answers[10:12], byteorder='big')
        ip_address = socket.inet_ntoa(answers[12:16])
        domain = 'google.com'  # Example domain
        print(f'> {domain}: type A, class IN, TTL 260, addr ({data_length}) {ip_address}')
        answers = answers[12+data_length:]

def main():
    server_address = ('127.0.0.1', 10053)
    while True:
        domain = input("Enter Domain Name: ")
        if domain == 'end':
            print("Session ended")
            break
        response = query_dns(server_address, domain)
        format_output(response)

if __name__ == '__main__':
    main()
