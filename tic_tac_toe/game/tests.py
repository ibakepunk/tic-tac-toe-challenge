from django.test import TestCase
import json
# Create your tests here.

class TestCreateGame(TestCase):
    def test_create(self):
        resp = self.client.post('/api/games/', {'players': ['karl', 'paul']}, 'application/json')
        self.assertEqual(resp.status_code, 200)
        game = resp.json()
        self.assertEqual(game['x_player'], 'karl')
        self.assertEqual(game['o_player'], 'paul')


class TestUpdateGame(TestCase):
    def test_does_not_exist(self):
        resp = self.client.post('/api/games/42/', {'players': ['karl', 'paul']}, 'application/json')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.json(), {'errors': {'error_code': 'game_not_found'}})

    def test_x_wins(self):
        resp = self.client.post('/api/games/', {'players': ['karl', 'paul']}, 'application/json')
        game_id = resp.json()['id']
        board = [['x', None, None],
                 [None, None, None],
                 [None, None, None]]
        resp = self.client.post(f'/api/games/{game_id}/', 
                                {'updated_by': 'karl', 'board': board}, 
                                'application/json')
        
        self.assertEqual(resp.json()['board'], board)
        self.assertEqual(resp.status_code, 200)

        board[0][1] = 'o'
        resp = self.client.post(f'/api/games/{game_id}/', 
                                {'updated_by': 'paul', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.json()['board'], board)

        board[1][1] = 'x'
        resp = self.client.post(f'/api/games/{game_id}/', 
                                {'updated_by': 'karl', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.json()['board'], board)

        board[1][0] = 'o'
        resp = self.client.post(f'/api/games/{game_id}/', 
                                {'updated_by': 'paul', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.json()['board'], board)

        board[2][2] = 'x'
        resp = self.client.post(f'/api/games/{game_id}/', 
                                {'updated_by': 'karl', 'board': board}, 
                                'application/json')
        game = resp.json()
        self.assertEqual(game['board'], board)
        self.assertEqual(game['updated_by'], 'karl')
        self.assertEqual(game['status'], 'x')

    def test_draw(self):
        resp = self.client.post('/api/games/', {'players': ['karl', 'paul']}, 'application/json')
        game_id = resp.json()['id']
        board = [['x', None, None],
                 [None, None, None],
                 [None, None, None]]
        resp = self.client.post(f'/api/games/{game_id}/', 
                                {'updated_by': 'karl', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['board'], board)

        board[0][1] = 'o'
        resp = self.client.post(f'/api/games/{game_id}/', 
                                {'updated_by': 'paul', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['board'], board)

        board[1][1] = 'x'
        resp = self.client.post(f'/api/games/{game_id}/', 
                                {'updated_by': 'karl', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['board'], board)

        board[1][0] = 'o'
        resp = self.client.post(f'/api/games/{game_id}/', 
                                {'updated_by': 'paul', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['board'], board)

        board[2][1] = 'x'
        resp = self.client.post(f'/api/games/{game_id}/', 
                                {'updated_by': 'karl', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.status_code, 200)

        board[0][2] = 'o'
        resp = self.client.post(f'/api/games/{game_id}/', 
                                {'updated_by': 'paul', 'board': board}, 
                                'application/json')
        
        self.assertEqual(resp.status_code, 200)

        board[2][0] = 'x'
        resp = self.client.post(f'/api/games/{game_id}/', 
                                {'updated_by': 'karl', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.status_code, 200)
        
        board[2][2] = 'o'
        resp = self.client.post(f'/api/games/{game_id}/', 
                                {'updated_by': 'paul', 'board': board}, 
                                'application/json')
        
        self.assertEqual(resp.status_code, 200)

        board[1][2] = 'x'
        resp = self.client.post(f'/api/games/{game_id}/', 
                                {'updated_by': 'karl', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.status_code, 200)
        
        game = resp.json()
        self.assertEqual(game['board'], board)
        self.assertEqual(game['updated_by'], 'karl')
        self.assertEqual(game['status'], 'draw')

class TestList(TestCase):
    def setUp(self):
        resp = self.client.post('/api/games/', {'players': ['karl', 'paul']}, 'application/json')
        self.game_id = resp.json()['id']
        self.client.post('/api/games/', {'players': ['alice', 'bob']}, 'application/json')
    
    def test_get_list(self):
        resp = self.client.get('/api/games/')
        self.assertEqual(resp.status_code, 200)
        games = resp.json()
        self.assertEqual(games['count'], 2)
        self.assertEqual(len(games['objects']), 2)

    def test_get_one(self):
        resp = self.client.get(f'/api/games/{self.game_id}/')
        game = resp.json()
        self.assertEqual(game['id'], self.game_id)
        self.assertEqual(game['x_player'], 'karl')
        self.assertEqual(game['o_player'], 'paul')
