from operator import truediv
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category, Comment
from django.contrib.auth.models import User


class TestView(TestCase):  # TestCase를 이용한 방식은 실제 데이터베이스가 아닌 가상의 데이터베이스를 새로 만들어 테스트
    def setUp(self):
        self.client = Client()
        self.user_trump=User.objects.create_user(username='trump', password='bark4689')
        self.user_obama=User.objects.create_user(username='obama', password='bark4689')
        self.user_obama.is_staff=True
        self.user_obama.save()
        
        self.category_programming=Category.objects.create(name='programming', slug='programming')
        self.category_music=Category.objects.create(name='music', slug='music')
        
        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
            category=self.category_programming,
            author=self.user_trump,
        )
        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            category=self.category_music,
            author=self.user_obama,
        )
        self.post_003 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='카테코리가 없습니다.',
            author=self.user_obama,
        )
        
        self.comment_001=Comment.objects.create(
            post=self.post_001,
            author=self.user_obama,
            content='첫 번째 댓글입니다.'
        )
        
    def category_card_test(self, soup):
        categories_card=soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)
        
        
    def navbar_test(self, soup):   #내비게이션 바를 점검하는 함수       이거제꾸고 create post ㅗ싀 들어가봐
        navbar=soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)
        
        logo_btn=navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')
        
        home_btn=navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')
        
        blog_btn=navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')
        
        about_me_btn=navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def test_post_list(self):
        self.assertEqual(Post.objects.count(), 3)
            
        #1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
        #1.2 정상적으로 페이지가 로드된다.
        #1.3 페이지 타이틀은 'blog'이다.
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.navbar_test(soup)
        self.category_card_test(soup)
        
        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)
  
        post_001_card=main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
            
        post_002_card=main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
            
        post_003_card=main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn(self.post_003.category.name, post_003_card.text)
            
        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)
            
        #포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response=self.client.get('/blog/')
        soup=BeautifulSoup(response.content, 'html.parser')
        main_area=soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)
            
           
    def test_post_detail(self):
            
        #1.2 그 포스트의 url은 'blog/1/'이다.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        #2 첫번째 포스트의 상세 페이지 테스트
        #2.1 첫번째 post url로 접근하면 정상적으로 작동한다(status code:200).
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.navbar_test(soup) 
        self.category_card_test(soup)
        
        #2.3 첫번째 포스트의 제목(title)이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(self.post_001.title, soup.title.text)
        
        #2.4 첫번째 포스트의 제목이 포스트 영역(post_area)에 있다.
        main_area=soup.find('div', id='main-area')
        post_area=main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)
        #2.5 첫번째 포스트의 작성자(author)가 포스트 영역에 있다.
        self.assertIn(self.user_trump.username.upper(), post_area.text)  
        
        #2.6 첫번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(self.post_001.content, post_area.text)
        
        comments_area=soup.find('div', id='comment-area')
        comment_001_area=comments_area.find('div', id='comment-1')
        self.assertIn(self.comment_001.author.username, comment_001_area.text)
        self.assertIn(self.comment_001.content, comment_001_area.text)
        
    def test_create_post(self):
        #로그인하지 않으면 status code가 200이면 안된다.
        response=self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)
        #로그인을 한다.
        self.client.login(username='trump', password='bark4689')
        response=self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)
            
        self.client.login(username='obama', password='bark4689')
            
        response=self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')
        
        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area=soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)
            
        self.client.post(
            '/blog/create_post/',
            {
                'title' : 'Post Form 만들기',
                'content' : "Post Form 페이지를 만듭시다.",
            }
        )
        self.assertEqual(Post.objects.count(), 4)
        last_post=Post.objects.last()
        self.assertEqual(last_post.title, "Post Form 만들기")
        self.assertEqual(last_post.author.username, 'obama')
            
    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)
            
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup) 
        self.category_card_test(soup)
            
        self.assertIn(self.category_programming.name, soup.h1.text)
        
        main_area=soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)  
        self.assertNotIn(self.post_003.title, main_area.text) 
            
    def test_update_post(self) :
        update_post_url=f'/blog/update_post/{self.post_003.pk}'
        
        #로그인하지 않은 경우
        response=self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)
        
        #로그인은 했지만 작성자가 아닌 경우
        self.assertNotEqual(self.post_003.author, self.user_trump)
        self.client.login(
            username=self.user_trump.username,
            password='bark4689'
        )
        response=self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)
        
        #작성자(obama)가 접근하는 경우
        self.client.login(
            username=self.post_003.author.username,
            password='bark4689'
        )
        
        response=self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')
        
        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area=soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)
        
        response=self.client.post(
            update_post_url,
            {
                'title' : '세 번째 포스트를 수정했습니다. ',
                'content': '안녕 세계? 우리는 하나!',
                'category' : self.category_music.pk
            },
            follow=True
        )
        soup=BeautifulSoup(response.content, 'html.parser')
        main_area=soup.find('div', id='main-area')
        self.assertIn('세 번째 포스트를 수정했습니다.', main_area.text)
        self.assertIn('안녕 세계? 우리는 하나!', main_area.text)
        self.assertIn(self.category_music.name, main_area.text)
        
    def test_comment_form(self):
        self.assertEqual(Comment.objects.count(), 1)  #댓글 하나 존재
        self.assertEqual(self.post_001.comment_set.count(), 1)  #post_001의 댓글 1개
        
        #로그인하지 않은 상태
        response=self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')
        
        comment_area=soup.find('div', id='comment-area')  #id가 comment-area인 div요소를 찾아 comment_area에 저장
        self.assertIn('Log in and leave a comment', comment_area.text)  #로그인하지 않은 상태이므로 'Log in and leave a comment'라는 문구가 보여야됨
        self.assertFalse(comment_area.find('form', id='comment-form'))  #로그인하지 않은 상태이므로 id가 comment-form인 form요소는 존재x
        
        #로그인한 상태 테스트
        self.client.login(username='obama', password='bark4689')
        response=self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')
        
        comment_area=soup.find('div', id='comment-area')
        self.assertNotIn('Log in and leave a comment', comment_area.text)  #로그인 했기 때문에 Log in and leave a comment라는 문구는 보이지 않는다.
        
        comment_form=comment_area.find('form', id='comment-form')
        self.assertTrue(comment_form.find('textarea', id='id_content'))  #로그인한 상태이므로 댓글 폼이 보이고 textarea도 있다.
        response=self.client.post(  #POST 방식으로 댓글 내용을 서버에 보낸다.(요청 결과를 response에 담는다.)
            self.post_001.get_absolute_url() + 'new_comment/',
            {
                'content': "오바마의 댓글입니다.",
            },
            follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(Comment.objects.count(), 2)  #POST방식으로 댓글을 하나 더 추가했으므로 전체 댓글 수는 2개
        self.assertEqual(self.post_001.comment_set.count(), 2) #post_001의 댓글 2개
        
        new_comment=Comment.objects.last()  #마지막으로 생성된 comment를 가져온다.
        
        soup=BeautifulSoup(response.content, 'html.parser')
        self.assertIn(new_comment.post.title, soup.title.text)  #POST방식으로 서버에 요청해 comment가 달린 포스트의 상세 페이지 리다이렉트(웹브라우저의 타이틀로 새로 만든 comment가 달린 포스트위 타이틀이 나타남)
        
        comment_area=soup.fine('div', id='comment-area')
        new_comment_div=comment_area.find('div', id=f'comment-{new_comment.pk}')  #새로 만든 comment의 내용과 작성자가 나타남
        self.assertIn('obama', new_comment_div.text)
        self.assertIn('오바마의 댓글입니다.', new_comment_div.text)
        
    def test_comment_update(self):
        comment_by_trump=Comment.objects.create(
            post=self.post_001,
            author=self.user_trump,
            content='트럼프의 댓글입니다.'
        )
        
        response=self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')
        
        comment_area=soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-update-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))
        
        #로그인한 상태
        self.client.login(username='obama', password='bark4689')
        response=self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')
        
        comment_area=soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))
        comment_001_update_btn=comment_area.find('a', id='comment-1-update-btn')
        self.assertIn('edit', comment_001_update_btn.text)
        self.assertEqual(comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')
        
        self.assertIn('edit', comment_001_update_btn.text)
        self.assertEqual(comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')
        response=self.client.get('/blog/update_comment/1/')
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')
        
        self.assertEqual('Edit Comment - Blog', soup.title.text)
        update_comment_form=soup.find('form', id='comment-form')
        content_textarea=update_comment_form.find('textarea', id='id_content')
        self.assertIn(self.comment_001.content, content_textarea.text)
        
        response=self.client.post(
            f'/blog/update_comment/{self.comment_001.pk}/',
            {
                'content': "오바마의 댓글을 수정합니다.",
            },
            follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')
        comment_001_div=soup.find('div', id='comment-1')
        self.assertIn('오바마의 댓글을 수정합니다.', comment_001_div.text)
        self.assertIn('Updated: ', comment_001_div.text)
        
    def test_delete_comment(self) :
        comment_by_trump=Comment.objects.create(
            post=self.post_001,
            author=self.user_trump,
            content='트럼프의 댓글입니다.'
        )
        
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2)
        
        #로그인하지 않은 상태
        response=self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')
        
        comment_area=soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-delete-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-delete-btn'))
        
        #trunp로 로그인한 상태
        self.client.login(username='trump', password='bark4689')
        response=self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')
        
        comment_area=soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-delete-btn'))
        comment_002_delete_modal_btn=comment_area.find('a', id='comment-2-delete-moda;-btn')
        self.assertIn('delete', comment_002_delete_modal_btn.text)
        self.assertEqual(comment_002_delete_modal_btn.attrs['data-target'], '#deleteCommentModal-2')
        
        delete_comment_modal_002=soup.find('div', id='deleteCommentModal-2')
        self.assertIn('Are you Sure?', delete_comment_modal_002.text)
        really_delete_btn_002=delete_comment_modal_002.find('a')
        self.assertIn('Delete', really_delete_btn_002.text)
        self.assertEqual(really_delete_btn_002.attrs['href'], '/blog/delete_comment/2/')
        
        response=self.client.get('/blog/delete_comment/2/', follow=True)
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')
        self.assertIn(self.post_001.title, soup.title.text)
        comment_area=soup.find('div', id='comment-area')
        self.assertNotIn('트럼프의 댓글입니다.', comment_area.text)
        
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post_001.comment_set.count(), 1)