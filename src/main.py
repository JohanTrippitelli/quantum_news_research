# main.py
import sys
import yaml
import scrape

def main(yaml_file, site_name, human_mode):
    # Load configuration from the provided YAML file
    try:
        with open(yaml_file, 'r') as file:
            config = yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading YAML file: {e}")
        sys.exit(1)
    
    # Check if the requested site is in the configuration
    if site_name not in config:
        print(f"Site '{site_name}' not found in configuration.")
        sys.exit(1)
    
    site_config = config[site_name]
    # Call the scraping function with the selected configuration and human mode flag
    scrape.scrape_site(site_config, human_mode)

if __name__ == '__main__':
    args = sys.argv[1:]
    human_mode = False
    # Look for the optional -hm flag and remove it from arguments if present
    if "-hm" in args:
        human_mode = True
        args.remove("-hm")
    
    if len(args) != 2:
        print("Usage: python main.py <yaml_file> <site_name> [-hm]")
        sys.exit(1)
    
    yaml_file, site_name = args
    main(yaml_file, site_name, human_mode)
