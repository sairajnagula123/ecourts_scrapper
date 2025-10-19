# main.py
import argparse
from scraper import search_case_by_cnr, download_cause_list

def main():
    parser = argparse.ArgumentParser(description="eCourts Scraper CLI")
    parser.add_argument("--cnr", help="Search case by CNR number")
    parser.add_argument("--district", help="Download cause list for district")
    args = parser.parse_args()

    if args.cnr:
        search_case_by_cnr(args.cnr)
    elif args.district:
        download_cause_list(args.district)
    else:
        print("⚠️ Please use --cnr <CNR_NUMBER> or --district <DISTRICT_NAME>")

if __name__ == "__main__":
    main()
