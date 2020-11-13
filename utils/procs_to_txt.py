import argparse

import mechanize as me

def _iclr(page_data):
    import json
    papers = json.loads(page_data)
    titles = [paper['content']['title'] for paper in papers]
    return titles

def _cvpr(page_data):
    tree_root = me._html.content_parser(page_data)
    body = list(tree_root)[1]
    content = list(body)[2]
    papers = list(list(content)[1])
    titles = []
    for paper in papers:
        if paper.tag != "dt": continue
        items = list(paper)
        titles.append(list(items)[1].text)
    return titles

def _neurips(page_data):
    tree_root = me._html.content_parser(page_data)
    titles = []
    body = list(tree_root)[1]
    for elem in list(body):
        if elem.tag == "div" and "class" in elem.attrib and elem.attrib["class"] == "container pull-left":
            accepted_papers = list(list(list(elem)[1])[4])[1]
            assert 'NeurIPS 2020 Accepted Papers' in list(accepted_papers)[0].text
            for elem in list(accepted_papers):
                if elem.tag != "p": continue
                paper_title = list(elem)[0]
                if paper_title.tag != "b": continue
                titles.append(format_title(paper_title.text))
    return titles

def format_title(title):
    return title.replace("$", "").strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Conference Proceedings Scraper',
        epilog = 'lol p4p3rz', add_help = 'How to use',
        prog = 'python procs_to_txt.py <options>')

    # Required arguments.
    parser.add_argument("-u", "--url", required = True,
        help = "URL to the list of conference proceedings.")
    parser.add_argument("-c", "--conf", required = True, choices = ["neurips", "iclr", "cvpr"],
        help = "Name of the conference. SUPPORTED: [neurips, iclr, cvpr]")

    # Optional arguments.
    parser.add_argument("-o", "--output", default = None,
        help = "Output file containing paper title content, one per line. [DEFAULT: None]")

    # NeurIPS 2020: https://neurips.cc/Conferences/2020/AcceptedPapersInitial
    # CVPR 2020: 
    # - Day 1: https://openaccess.thecvf.com/CVPR2020?day=2020-06-16
    # - Day 2: https://openaccess.thecvf.com/CVPR2020?day=2020-06-17
    # - Day 3: https://openaccess.thecvf.com/CVPR2020?day=2020-06-18
    # ICLR: 2020: https://iclr.cc/virtual_2020/papers.json

    # Parse out the arguments.
    args = vars(parser.parse_args())
    
    # Set up the browser.
    br = me.Browser()
    response = br.open(args['url'])
    page_data = response.get_data()

    # Which one are we parsing out?
    titles = globals()[f"_{args['conf']}"](page_data)
    
    # Write the titles out to a file.
    fname = f"{args['conf']}.txt" if not args['output'] else args['output']
    with open(fname, "w") as f:
        f.write("\n".join(titles))

    # All done!
    print(f"Wrote {len(titles)} paper titles to {fname}.")
