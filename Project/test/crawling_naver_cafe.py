import time
from selenium import webdriver
import csv
import pandas as pd
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

def save_dict_to_csv(data, fp):
    df = pd.DataFrame(data)
    if not os.path.exists(fp):
        df.to_csv(fp, index=False, mode='w', encoding='utf-8-sig')
    else:
        df.to_csv(fp, index=False, mode='a', encoding='utf-8-sig', header=False)
    return

if __name__=="__main__":
    # Naver login url / your id / your passward
    url='https://nid.naver.com/nidlogin.login'
    id_ = 'hmg_de'
    pw = 'hmg_dehmg_de'
        
    browser = webdriver.Chrome()
    browser.get(url)

    browser.implicitly_wait(2)

    # Naver login 네이버 로그인
    browser.execute_script("document.getElementsByName('id')[0].value=\'"+ id_ + "\'")
    browser.execute_script("document.getElementsByName('pw')[0].value=\'"+ pw + "\'")
    browser.find_element(by=By.XPATH,value='//*[@id="log.login"]').click()
    time.sleep(1)
        
    # wanted naver cafe url
    base_url='https://cafe.naver.com/allfm01'

    # wanted keyword list
    Search_Keyword = ['iccu']

    results = []

    for search_key in Search_Keyword:
        # Connecting Naver Cafe 네이버 카페 접속
        browser.get(base_url)

        # Input search keyword 검색어 입력
        search_box = browser.find_element(By.ID, "topLayerQueryInput")
        search_box.send_keys(search_key)

        # Click search box 검색 버튼 클릭
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)
        
        # driver창의 frame 을 iframe의 태그인 cafe_main으로 바꿔주기
        browser.switch_to.frame("cafe_main")

        # Click Dropdown menu 검색 옵션 드롭다운 메뉴 클릭
        search_option_dropdown = browser.find_element(By.ID, "divSearchByTop")
        search_option_dropdown.click()
        time.sleep(1)

        # Select option 'only title' '제목만' 옵션 선택
        title_only_option = browser.find_element(By.XPATH, "//a[contains(text(), '제목만')]")
        title_only_option.click()
        time.sleep(2)

        # Click search box 검색 버튼 클릭
        search_btn = browser.find_element(By.XPATH, "//button[contains(text(), '검색')]")
        search_btn.click()
        time.sleep(2)

        # Select option 'get 50 posts each' (1)/ "50개씩" 보기 옵션을 선택하기 위한 드롭다운 메뉴 클릭
        dropdown_menu = browser.find_element(By.ID, "listSizeSelectDiv")
        dropdown_menu.click()
        time.sleep(1)  # 드롭다운 메뉴 옵션들이 표시될 때까지 대기

        # Select option 'get 50 posts each' (2)/"50개씩" 옵션 선택
        fifty_option = browser.find_element(By.XPATH, "//a[contains(text(), '50개씩')]")
        fifty_option.click()
        time.sleep(2)  # 옵션 선택 후 페이지 로딩 대기


        #TODO 아래 코드를 모두 while loop에 넣어서 날짜 조건 확인해야 함
        
        # 검색 결과 페이지에 대한 href
        page_links = browser.find_elements(By.CSS_SELECTOR, '.prev-next a')
        page_hrefs = [page_link.get_attribute('href') for page_link in page_links]
        
        ###
        page_idx = 0
        # 10개의 페이지에 대해
        for page_href in page_hrefs:
            if page_idx != 0:
                print("page_idx", page_idx)
                browser.get(page_href)
                browser.implicitly_wait(2)
                browser.switch_to.frame("cafe_main")
                
            else: 
                pass

            # BeautifulSoup으로 HTML을 파싱
            soup = bs(browser.page_source, 'html.parser')

            # 해당 class를 가진 모든 게시글 링크들을 찾음
            article = soup.select('div.inner_list a.article')
            titles = [link.text.strip() for link in article]
            links = [link['href'] for link in article]
                
            post_ids = []
            contents = []
            likes = []
            authors = []
            views = []
            created_ats = []
            urls = []
            updated_ats = []
            post_titles = []
            
            # 50개의 글에 대해
            for title, link in zip(titles[:1], links[:1]):
                retries = 1 # how many retries / 해당 글을 몇번 들어갈건지 선정
                success = False # 글 접속 성공여부

                while retries > 0 and not success:
                    fail = False

                    cmt_authors = []
                    cmt_contents = []
                    cmt_post_ids = []    
                    cmt_created_ats = []
                    cmt_updated_ats = []

                    # 게시글의 링크로 이동
                    browser.get('https://cafe.naver.com' + link)
                    time.sleep(3)
                    browser.switch_to.frame("cafe_main")

                    # 해당 페이지의 HTML 소스 가져오기
                    page_source = browser.page_source

                    # BeautifulSoup으로 HTML 파싱
                    soup_article = bs(page_source, 'html.parser')

                    # Date
                    try: # 등급 문제로 게시물을 읽을 수 없는 경우, 다음 게시물로 이동
                        date = soup_article.find('div', class_='article_info').find('span', class_='date').text.strip()
                    except:
                        fail = True
                        break

                    # Nickname
                    nickname_div = soup_article.find('div', class_='article_writer')
                    nickname_strong = nickname_div.find('strong', class_='user')
                    nickname = nickname_strong.text.strip()

                    # Views
                    views_elem = browser.find_element(By.CLASS_NAME, 'article_info')
                    view = views_elem.find_element(By.CLASS_NAME, 'count').text.replace("조회 ", '')
                                    
                    # Content
                    content_elem = browser.find_elements(By.CLASS_NAME, 'se-fs-')
                    content = ""
                    for element in content_elem:
                        content+=element.text
                    
                    # Post id
                    post_id = int(soup_article.find('div', class_='text_area').find(class_='naver-splugin').get('data-url').split('/')[-1])
                    retries -= 1  # 재시도 횟수 감소

                    # Likes
                    like = browser.find_element(By.CLASS_NAME, 'u_cnt._count').text
                    
                    # comments
                    cmt_elem = browser.find_elements(By.CLASS_NAME, 'comment_box')
                    
                    if len(cmt_elem) != 0:
                        for elem in cmt_elem:
                            try:
                                # 댓글에 내용이 없는 경우, 다음 댓글로 이동                   
                                cmt_content = elem.find_element(By.CLASS_NAME, 'text_comment').get_attribute('textContent').strip()
                            except:
                                continue
                            cmt_nickname = elem.find_element(By.CLASS_NAME, 'comment_nickname').get_attribute('textContent').strip()
                            cmt_created_at = elem.find_element(By.CLASS_NAME, 'comment_info_date').get_attribute('textContent').strip()
                            cmt_likes = elem.find_element(By.CLASS_NAME, 'u_cnt._count').text

                            cmt_post_ids.append(post_id)                        
                            cmt_authors.append(cmt_nickname)
                            cmt_contents.append(cmt_content)
                            cmt_created_ats.append(cmt_created_at)
                            cmt_updated_ats.append(None)

                        comment_data = {"post_id": cmt_post_ids, "cmt_content": cmt_contents, "cmt_author": cmt_authors, "cmt_created_at": cmt_created_ats, \
                                        "cmt_updated_at": cmt_updated_ats}
                        save_dict_to_csv(comment_data, "cmt.csv")

                if not fail:
                    post_titles.append(title)
                    post_ids.append(post_id)
                    created_ats.append(date)
                    updated_ats.append(None)
                    authors.append(nickname)
                    contents.append(content)
                    urls.append('https://cafe.naver.com' + link)
                    views.append(view)
                    likes.append(like)
                    # results.append({
                    #     'title': title,
                    #     'id': post_id,
                    #     'Date': date,
                    #     'Nickname': nickname,
                    #     'contents': content,
                    #     'url': 'https://cafe.naver.com' + link
                    # })
            post_data = {"id": post_ids, "title": post_titles, 'content': contents, 'likes': likes, 'url': urls, \
                'author': authors, 'views': views, "created_at": created_ats, "updated_at": updated_ats}   
            
            save_dict_to_csv(post_data, "post.csv")
            page_idx = (page_idx + 1) % 10
