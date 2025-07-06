import whois # You'll need to install this library: pip install python-whois
import dns.resolver # You'll need to install this library: pip install dnspython

def perform_whois_lookup(domain):
    """
    Performs a WHOIS lookup for the given domain and returns the registration information.
    """
    print(f"\n--- WHOIS Information for {domain} ---")
    try:
        # Perform the WHOIS query
        domain_info = whois.whois(domain)

        if domain_info:
            # Print key WHOIS fields if available
            print(f"Domain Name: {domain_info.domain_name}")
            print(f"Registrar: {domain_info.registrar}")
            print(f"WHOIS Server: {domain_info.whois_server}")
            print(f"Referral URL: {domain_info.referral_url}")
            print(f"Creation Date: {domain_info.creation_date}")
            print(f"Expiration Date: {domain_info.expiration_date}")
            print(f"Last Updated: {domain_info.updated_date}")
            print(f"Name Servers: {domain_info.name_servers}")
            print(f"Status: {domain_info.status}")
            
            # Print registrant details if available
            if domain_info.registrant_name:
                print("\nRegistrant Details:")
                print(f"  Name: {domain_info.registrant_name}")
                print(f"  Organization: {domain_info.registrant_organization}")
                print(f"  Country: {domain_info.registrant_country}")
            else:
                print("\nRegistrant details not explicitly available or redacted.")

            # Print raw WHOIS text for full details
            print("\n--- Raw WHOIS Data ---")
            print(domain_info.text)
        else:
            print(f"No WHOIS information found for {domain}.")
    except whois.exceptions.WhoisCommandFailed as e:
        print(f"Error: WHOIS query failed for {domain}. This might be due to an invalid domain, rate limiting, or server issues.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during WHOIS lookup: {e}")

def perform_nslookup(domain):
    """
    Performs an NSLOOKUP (DNS query) for the given domain and returns its IP addresses.
    """
    print(f"\n--- NSLOOKUP (DNS Information) for {domain} ---")
    try:
        # Resolve A records (IPv4 addresses)
        a_records = dns.resolver.resolve(domain, 'A')
        print("IPv4 Addresses (A records):")
        if a_records:
            for ip_val in a_records:
                print(f"  {ip_val.address}")
        else:
            print("  No IPv4 addresses found.")

        # Resolve AAAA records (IPv6 addresses)
        try:
            aaaa_records = dns.resolver.resolve(domain, 'AAAA')
            print("\nIPv6 Addresses (AAAA records):")
            if aaaa_records:
                for ip_val in aaaa_records:
                    print(f"  {ip_val.address}")
            else:
                print("  No IPv6 addresses found.")
        except dns.resolver.NoAnswer:
            print("\nNo IPv6 addresses (AAAA records) found.")
        except Exception as e:
            print(f"Error resolving IPv6 addresses: {e}")

        # Resolve MX records (Mail Exchangers)
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            print("\nMail Exchange (MX) Records:")
            if mx_records:
                for mx_val in mx_records:
                    print(f"  Preference: {mx_val.preference}, Mail Server: {mx_val.exchange}")
            else:
                print("  No MX records found.")
        except dns.resolver.NoAnswer:
            print("\nNo Mail Exchange (MX) records found.")
        except Exception as e:
            print(f"Error resolving MX records: {e}")

        # Resolve NS records (Name Servers)
        try:
            ns_records = dns.resolver.resolve(domain, 'NS')
            print("\nName Server (NS) Records:")
            if ns_records:
                for ns_val in ns_records:
                    print(f"  {ns_val.target}")
            else:
                print("  No NS records found.")
        except dns.resolver.NoAnswer:
            print("\nNo Name Server (NS) records found.")
        except Exception as e:
            print(f"Error resolving NS records: {e}")

    except dns.resolver.NXDOMAIN:
        print(f"Error: Domain '{domain}' does not exist (NXDOMAIN).")
    except dns.resolver.NoAnswer:
        print(f"No A records found for '{domain}'.")
    except dns.resolver.Timeout:
        print(f"Error: DNS query timed out for {domain}.")
    except Exception as e:
        print(f"An unexpected error occurred during NSLOOKUP: {e}")

if __name__ == "__main__":
    print("--- Domain Information Tool (WHOIS & NSLOOKUP) ---")
    print("This tool fetches registration details and IP addresses for a given domain.")
    
    while True:
        domain_input = input("\nEnter a domain name (e.g., example.com) or 'exit' to quit: ").strip().lower()
        
        if domain_input == 'exit':
            print("Exiting tool. Goodbye!")
            break
        elif not domain_input:
            print("Domain name cannot be empty. Please try again.")
            continue
        
        # Basic validation for domain format (can be expanded)
        if '.' not in domain_input:
            print("Invalid domain format. Please include a top-level domain (e.g., .com, .org).")
            continue

        print(f"\nProcessing domain: {domain_input}")
        
        # Perform WHOIS lookup
        perform_whois_lookup(domain_input)
        
        # Perform NSLOOKUP
        perform_nslookup(domain_input)
        
        print("\n" + "="*60) # Separator for next query
