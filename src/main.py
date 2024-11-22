import argparse
from config.settings import load_config
from core.matcher import process_resumes
from utils.file_handler import get_pdf_files, read_job_description
from output.report_generator import generate_final_report
from core.ai_client import AIClient

def parse_args():
    parser = argparse.ArgumentParser(description="Resume Matcher")
    parser.add_argument("--sans-serif", action="store_true", help="Use sans-serif font preset")
    parser.add_argument("--serif", action="store_true", help="Use serif font preset")
    parser.add_argument("--mono", action="store_true", help="Use monospace font preset")
    parser.add_argument("--pdf", action="store_true", help="Generate PDF files")
    parser.add_argument("--api_key", required=True, help="API key for the service")
    parser.add_argument("--base_url", required=True, help="Base URL for the API service")
    parser.add_argument("job_desc_file", nargs="?", 
                       default="data/job_descriptions/job_description.txt")
    parser.add_argument("pdf_folder", nargs="?", 
                       default="data/resumes")
    return parser.parse_args()

def main():
    args = parse_args()
    config = load_config()
    
    ai_client = AIClient(api_key=args.api_key, base_url=args.base_url)
    
    job_desc = read_job_description(args.job_desc_file)
    
    pdf_files = get_pdf_files(args.pdf_folder)
    
    results = process_resumes(
        job_desc=job_desc,
        pdf_files=pdf_files,
        font_styles={
            'sans-serif': args.sans_serif,
            'serif': args.serif,
            'mono': args.mono
        },
        generate_pdf=args.pdf,
        ai_client=ai_client
    )
    
    generate_final_report(results)

if __name__ == "__main__":
    main() 