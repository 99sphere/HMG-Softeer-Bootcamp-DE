from urllib import parse
page_num=1

keyword = '코나%20화재'
keyword = parse.quote_plus(keyword)

board_url = f'https://cafe.naver.com/allfm01?iframe_url=/ArticleSearchList.nhn%3Fsearch.clubid=21771803%26search.media=0%26\
    search.searchdate=all%26search.exact=%26search.include=%26userDisplay=50%26search.exclude=%26search.option=0%26search.sortBy=date%26search.searchBy=0%26search.includeAll=%26\
        search.query={keyword}%26search.viewtype=title%26search.page={page_num}'

print(keyword, "\n", board_url)
