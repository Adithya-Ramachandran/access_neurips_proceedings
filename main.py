import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path


def get_data_from_web(soup, base_url_paper, csv_file_name, path_to_paper)->None:

    # Open CSV file to store results
    with open(csv_file_name, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)
        writer.writerow(["number", "title", "authors", "paper_url", "local_location", "type"])  # headers for the csv file

        counter = 0  # counter for the file name - each downloaded paper is given a unique integer instead of the long name

        "------------------------------- conference papers ----------------------------------------------------------------"
        for paper in soup.find_all("li", class_="conference"):  # find all list with tag 'conference'

            title = paper.find("a").text.strip()  # get the title of the paper
            authors = [author.text.strip() for author in paper.contents[3]][0].split(',')  # get author names
            paper_url = base_url_paper + paper.find("a")["href"]  # paper specific url

            response_paper_url = requests.get(paper_url)  # get the response for a specific paper
            soup_paper_url = BeautifulSoup(response_paper_url.text, 'html.parser')

            pdf_link_tag = soup_paper_url.find("a", string="Paper")  # get the pdf link

            if pdf_link_tag:  # if there is tag

                pdf_url = base_url_paper + pdf_link_tag["href"]  # get the pdf's url for a specific paper
                pdf_response = requests.get(pdf_url)  # get response

                with open(Path(Path.cwd(), "data", "papers", str(counter) + ".pdf"), "wb") as file_pdf:  # save file
                    file_pdf.write(pdf_response.content)

                # Write to CSV - update csv with information about the downloaded file
                writer.writerow([counter,
                                 title,
                                 authors,
                                 paper_url,
                                 Path(path_to_paper, str(counter) + ".pdf"),
                                 "conference"])

                print(f"Counter: {counter}")
                counter += 1

            else:
                print("PDF link not found.")

        "------------------------------- Datasets and Benchmarks ----------------------------------------------------------------"

        for paper in soup.find_all("li", class_="datasets_and_benchmarks_track"):   # find all list with tag 'datasets_and_benchmarks_track'

            title = paper.find("a").text.strip()  # get the title of the paper
            authors = [author.text.strip() for author in paper.contents[3]][0].split(',')  # get author names
            paper_url = base_url_paper + paper.find("a")["href"]  # paper specific url

            response_paper_url = requests.get(paper_url)  # get the response for a specific paper
            soup_paper_url = BeautifulSoup(response_paper_url.text, 'html.parser')

            pdf_link_tag = soup_paper_url.find("a", string="Paper")  # get the pdf link

            if pdf_link_tag:  # if there is tag

                pdf_url = base_url_paper + pdf_link_tag["href"]  # get the pdf's url for a specific paper
                pdf_response = requests.get(pdf_url)  # get response

                with open(Path(Path.cwd(), "data", "papers", str(counter) + ".pdf"), "wb") as file_pdf:  # save file
                    file_pdf.write(pdf_response.content)

                # Write to CSV - update csv with information about the downloaded file
                writer.writerow([counter,
                                 title,
                                 authors,
                                 paper_url,
                                 Path(path_to_paper, str(counter) + ".pdf"),
                                 "datasets_and_benchmarks_track"])

                print(f"Counter: {counter}")
                counter += 1

            else:
                print("PDF link not found.")

def main():
    year = 2024  # year of Neurips - tested for 2023, 2024
    url = f"https://papers.nips.cc/paper_files/paper/{str(year)}"  # url for the conference proceeding
    base_url_paper = f"https://papers.nips.cc"  # url base for a specific paper

    response = requests.get(url)   # Send GET request to fetch the page
    soup = BeautifulSoup(response.text, 'html.parser')

    csv_path = "neurips_2024_papers.csv"  # output file - path for a csv file to store information about a paper
    path_to_paper = Path(Path.cwd(), "data", "papers")  #  path to store papers

    get_data_from_web(soup, base_url_paper, csv_path, path_to_paper)


if __name__ == '__main__':
    main()



