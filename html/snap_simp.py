from bs4 import BeautifulSoup

from python.objects.snap import Snap

def get_snaps_from_snap_history_html_file(relative_file_name: str):
    with open(relative_file_name, 'r') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    body = soup.find('body')
    table = soup.find('table')
    snaps = []

    rows = table.find_all('tr')

    for row in rows:
        cols = row.find_all('td')

        # Make sure there are exactly 3 columns
        if len(cols) == 3:
            # Create a new Snap object and add it to the list
            snap = Snap(cols[0].text, cols[1].text, cols[2].text)
            snaps.append(snap)

    # Print all the snaps
    for snap in snaps:
        print(snap)


if __name__ == '__main__':
    # todo argparse this but default to this
    get_snaps_from_snap_history_html_file('snap_history.html') 