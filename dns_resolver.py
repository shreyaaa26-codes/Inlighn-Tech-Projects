import dns.resolver

target_domain = 'youtube.com'
records_type = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'SOA']

resolver = dns.resolver.Resolver()

for record_type in records_type:
    try:
        answer = resolver.resolve(target_domain, record_type)
        print(f"\n{record_type} records for {target_domain}")
        for data in answer:
            print(f"  {data}")
    except dns.resolver.NoAnswer:
        print(f"\nNo {record_type} records found for {target_domain}")
    except dns.resolver.NXDOMAIN:
        print(f"\nDomain {target_domain} does not exist.")
    except Exception as e:
        print(f"\nError fetching {record_type} records: {e}")
 
                