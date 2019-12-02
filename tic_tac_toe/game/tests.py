from django.test import TestCase
# Create your tests here.

class TestCreateGame(TestCase):
    def test_create(self):
        resp = self.client.post('/games/', {'players': ['karl', 'paul']}, 'application/json')
        print(resp.json())
        self.assertEqual(resp.status_code, 200)


class TestUpdateGame(TestCase):
    def test_x_wins(self):
        resp = self.client.post('/games/', {'players': ['karl', 'paul']}, 'application/json')
        game_id = resp.json()['id']
        board = [['x', None, None],
                 [None, None, None],
                 [None, None, None]]
        resp = self.client.post(f'/games/{game_id}/', 
                                {'updated_by': 'karl', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.json()['board'], board)
        self.assertEqual(resp.status_code, 200)

        board[0][1] = 'o'
        resp = self.client.post(f'/games/{game_id}/', 
                                {'updated_by': 'paul', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.json()['board'], board)

        board[1][1] = 'x'
        resp = self.client.post(f'/games/{game_id}/', 
                                {'updated_by': 'karl', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.json()['board'], board)

        board[1][0] = 'o'
        resp = self.client.post(f'/games/{game_id}/', 
                                {'updated_by': 'paul', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.json()['board'], board)

        board[2][2] = 'x'
        resp = self.client.post(f'/games/{game_id}/', 
                                {'updated_by': 'karl', 'board': board}, 
                                'application/json')
        game = resp.json()
        self.assertEqual(game['board'], board)
        self.assertEqual(game['updated_by'], 'karl')
        self.assertTrue(game['finished'])

    def test_draw(self):
        resp = self.client.post('/games/', {'players': ['karl', 'paul']}, 'application/json')
        game_id = resp.json()['id']
        board = [['x', None, None],
                 [None, None, None],
                 [None, None, None]]
        resp = self.client.post(f'/games/{game_id}/', 
                                {'updated_by': 'karl', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['board'], board)

        board[0][1] = 'o'
        resp = self.client.post(f'/games/{game_id}/', 
                                {'updated_by': 'paul', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['board'], board)

        board[1][1] = 'x'
        resp = self.client.post(f'/games/{game_id}/', 
                                {'updated_by': 'karl', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['board'], board)

        board[1][0] = 'o'
        resp = self.client.post(f'/games/{game_id}/', 
                                {'updated_by': 'paul', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['board'], board)

        board[2][2] = 'x'
        resp = self.client.post(f'/games/{game_id}/', 
                                {'updated_by': 'karl', 'board': board}, 
                                'application/json')
        self.assertEqual(resp.status_code, 200)
        game = resp.json()
        self.assertEqual(game['board'], board)
        self.assertEqual(game['updated_by'], 'karl')
        self.assertTrue(game['finished'])