from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from ..tools.http_tools import get_html


def date_str_to_date(date_str):
    """
    Convert "? [초 | 분 | 시간 | 일]전" to "20xx-xx-xx"
    """

    if '방금' in date_str:
        return datetime.now()
    elif '일' in date_str:
        num = int(re.findall(r"\d", date_str)[0])
        return datetime.now() - timedelta(days=num)
    elif '시간' in date_str:
        num = int(re.findall(r"\d", date_str)[0])
        return datetime.now() - timedelta(hours=num)
    elif '분' in date_str:
        num = int(re.findall(r"\d", date_str)[0])
        return datetime.now() - timedelta(minutes=num)
    elif '초' in date_str:
        num = int(re.findall(r"\d", date_str)[0])
        return datetime.now() - timedelta(seconds=num)
    else:
        if not re.match(r".*\..*\..*", date_str):
            raise Exception("It's doesn't match date format.")
        return datetime.strptime(date_str, "%Y.%m.%d").date()


class EndPageException(Exception):
    pass


class DogdripComment:
    """
    Attributes
    ---------
    nickname : str
        a nickname of the user
    content : str
        a content of the comment
    like_votes : str
        a number of the like votes
    date_str : Date
        a date text of the comment
    date : Date
        a regdate of the post
    """

    def __init__(self, nickname, content, like_votes, date_str):
        self.nickname = nickname
        self.content = content
        self.like_votes = int(like_votes)
        self.date_str = date_str
        self.date = date_str_to_date(date_str)

    def __str__(self):
        return "nickname:{}\ncontent:{}\nlike_votes:{}\ndate_str:{}\ndate:{}\n".format(self.nickname, self.content, self.like_votes, self.date_str, self.date)


class DogdripPost:
    """
    Attributes
    ---------
    num : str
        an id number of the post
    title : str
        a title of the post
    author : str
        an author of the post
    vote_num : str
        a number of votes of the post
    date_str: str
        a date text of the post
    date : Date
        a regdate of the post
    link:
        a link of the post

    Properties
    ---------
    comments(self)
        return a list of DogdripComment
    """

    def __init__(self, num, title, author, vote_num, date_str, link):
        self.num = num
        self.title = title
        self.author = author
        self.vote_num = int(vote_num)
        self.date_str = date_str
        self.date = date_str_to_date(date_str)
        self.link = link

    @property
    def comments(self):

        success_to_get = False

        while not success_to_get:
            source = get_html(self.link)
            sources = [source]

            # if there is pagination, append sources of other comments into sources list
            soup = BeautifulSoup(source, "html.parser")

            # if there is no 'comment', It's failed to fetch source
            # because it's too fast to request again.
            if soup.find("div", {"class": "comment"}) != None:
                success_to_get = True
            else:
                print("refetch")

        pagination = soup.find("div", {"class": "comment"}).find(
            "ul", {"class": "pagination"})
        if pagination:
            li_ets = pagination.findAll("li")

            # get source from page li elements
            for li_et in li_ets:
                if li_et.has_attr("href"):
                    sources.append(get_html(li_et["href"]))

        comments = []

        for source in sources:
            soup = BeautifulSoup(source, "html.parser")
            comment_list_div = soup.find("div", {"class": "comment-list"})
            comment_divs = comment_list_div.findAll(
                "div", {"class": "comment-item"})

            for comment_div in comment_divs:
                # nickname, content, like_votes, date_str, date
                nickname = comment_div.find(
                    "a", {"class": "link-reset"}).text.strip()
                content = comment_div.find(
                    "div", {"class": re.compile(r"comment_.*")})
                if not content:
                    content = ""  # if comment is deleted
                else:
                    content = content.text  # if comment is there
                like_votes = comment_div.find(
                    "span", {"class": "count"})
                if not like_votes:
                    like_votes = 0  # if comment is deleted
                else:
                    like_votes = like_votes.text.strip()  # if comment is there
                date_str = comment_div.find(
                    "div", {"class": "ed flex flex-right"}).find("span").text.strip()

                comments.append(DogdripComment(
                    nickname=nickname, content=content, like_votes=like_votes, date_str=date_str))

        return comments

    def __str__(self):
        return "num:{}\ntitle:{}\nauthor:{}\nvote_num:{}\ndate_str:{}\ndate:{}\nlink:{}\n".format(self.num, self.title, self.author, self.vote_num, self.date_str, self.date, self.link)


class DogdripScraper:
    """
    Attributes
    ---------
    __current_page : int
        current page

    Methods
    ---------
    next_page(self)
        parse next page
    __get_board_url(self, page)
        get url of the dogdrip board url by page

    Properties
    ---------
    posts(self)
        return a list of DogdripPost
    current_page(self)
        return current page

    """

    def __init__(self, page=1, next_page_step=1):
        """
        - Arguments
            page : start page number to parse
            next_page_step : number how many  add page when call next function
        """
        self.__current_page = page
        self.__next_page_step = next_page_step
        pass

    def __get_board_url(self, page):
        return "https://www.dogdrip.net/index.php?mid=dogdrip&page={0}".format(page)

    @property
    def posts(self):
        source = get_html(self.__get_board_url(self.__current_page))
        soup = BeautifulSoup(source, "html.parser")

        if soup.find("table").find("tbody").find("tr", {"class": "no_article"}):
            raise EndPageException

        posts_trs = soup.find("table").find("tbody").findAll("tr")

        posts = []

        for posts_tr in posts_trs:
            # num, title, author, vote_num, date_str, link
            num = posts_tr.find("td", {"class": "no"}).text.strip()
            title = posts_tr.find("td", {"class": "title"}).find(
                "span", {"class": "title-link"}).text.strip()
            author = posts_tr.find("td", {"class": "author"}).find(
                "a").text.strip()
            vote_num = posts_tr.find("td", {"class": "voteNum"}).text.strip()
            date_str = posts_tr.find("td", {"class": "time"}).text.strip()
            link = posts_tr.find("td", {"class", "title"}).find("a")["href"]

            # create DogdripPost and then add it to the post list.
            posts.append(DogdripPost(num=num, title=title, author=author,
                                     vote_num=vote_num, date_str=date_str, link=link))

        return posts

    @property
    def current_page(self):
        return self.__current_page

    def next_page(self):
        self.__current_page += self.__next_page_step
