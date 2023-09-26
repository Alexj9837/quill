import unittest
from app import app, db 

class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite3'  
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Test GET request to retrieve all Constitutional Conventions
    def test_get_conventions(self):
        response = self.app.get('/constitutional_conventions')
        self.assertEqual(response.status_code, 200)

    # Test GET request to retrieve a specific Constitutional Convention by ID
    def test_get_convention_by_id(self):
        response = self.app.get('/constitutional_conventions/1')
        self.assertEqual(response.status_code, 200)

    # Test POST request to create a new Constitutional Convention
    def test_create_convention(self):
        data = {
            "date": "2023-09-25",
            "location": "Test Location",
            "participants": "Test Participants"
        }
        response = self.app.post('/constitutional_conventions', json=data)
        self.assertEqual(response.status_code, 201)

    # Test PUT request to update an existing Constitutional Convention
    def test_update_convention_by_id(self):
        data = {
            "date": "2023-09-25",
            "location": "Updated Location",
            "participants": "Updated Participants"
        }
        response = self.app.put('/constitutional_conventions/1', json=data)
        self.assertEqual(response.status_code, 200)

    # Test DELETE request to delete an existing Constitutional Convention
    def test_delete_convention_by_id(self):
        response = self.app.delete('/constitutional_conventions/1')
        self.assertEqual(response.status_code, 204)

    # Similar tests for Committees endpoints
    def test_get_committees(self):
        response = self.app.get('/committees')
        self.assertEqual(response.status_code, 200)

    def test_get_committee_by_id(self):
        response = self.app.get('/committees/1')
        self.assertEqual(response.status_code, 200)

    def test_create_committee(self):
        data = {
            "committee_name": "Test Committee",
            "committee_members": "Test Members",
            "topics_covered": "Test Topics"
        }
        response = self.app.post('/committees', json=data)
        self.assertEqual(response.status_code, 201)

    def test_update_committee_by_id(self):
        data = {
            "committee_name": "Updated Committee",
            "committee_members": "Updated Members",
            "topics_covered": "Updated Topics"
        }
        response = self.app.put('/committees/1', json=data)
        self.assertEqual(response.status_code, 200)

    def test_delete_committee_by_id(self):
        response = self.app.delete('/committees/1')
        self.assertEqual(response.status_code, 204)

    def test_debates_routes(self):
        # Test POST request to create a debate
        response = self.app.post('/debates', json={
            "debate_date": "2023-09-01",
            "debate_location": "Test Location",
            "participants": "Test Participants",
            "debate_content": "Test Content",
            "committee_id": 1,
            "document_id": 1
        })
        self.assertEqual(response.status_code, 201)

        # Test GET request to retrieve all debates
        response = self.app.get('/debates')
        self.assertEqual(response.status_code, 200)
        debates = response.get_json().get("debates")
        self.assertEqual(len(debates), 1)

        # Test GET request to retrieve a specific debate
        debate_id = debates[0]['debate_id']
        response = self.app.get(f'/debates/{debate_id}')
        self.assertEqual(response.status_code, 200)

        # Test PUT request to update a debate
        response = self.app.put(f'/debates/{debate_id}', json={"debate_location": "Updated Location"})
        self.assertEqual(response.status_code, 200)
        updated_debate = response.get_json().get("debate")
        self.assertEqual(updated_debate['debate_location'], "Updated Location")

        # Test DELETE request to delete a debate
        response = self.app.delete(f'/debates/{debate_id}')
        self.assertEqual(response.status_code, 204)

    def test_documents_routes(self):
        # Test POST request to create a document
        response = self.app.post('/documents', json={
            "document_type": "Test Type",
            "author": "Test Author",
            "document_content": "Test Content"
        })
        self.assertEqual(response.status_code, 201)

        # Test GET request to retrieve all documents
        response = self.app.get('/documents')
        self.assertEqual(response.status_code, 200)
        documents = response.get_json().get("documents")
        self.assertEqual(len(documents), 1)

        # Test GET request to retrieve a specific document
        document_id = documents[0]['document_id']
        response = self.app.get(f'/documents/{document_id}')
        self.assertEqual(response.status_code, 200)

        # Test PUT request to update a document
        response = self.app.put(f'/documents/{document_id}', json={"author": "Updated Author"})
        self.assertEqual(response.status_code, 200)
        updated_document = response.get_json().get("document")
        self.assertEqual(updated_document['author'], "Updated Author")

        # Test DELETE request to delete a document
        response = self.app.delete(f'/documents/{document_id}')
        self.assertEqual(response.status_code, 204)

    def test_commentaries_routes(self):
        # Test POST request to create a commentary
        response = self.app.post('/commentaries', json={
            "author": "Test Author",
            "timestamp": "2023-09-01T12:00:00Z",
            "commentary_text": "Test Commentary",
            "debate_id": 1,
            "document_id": 1
        })
        self.assertEqual(response.status_code, 201)

        # Test GET request to retrieve all commentaries
        response = self.app.get('/commentaries')
        self.assertEqual(response.status_code, 200)
        commentaries = response.get_json().get("commentaries")
        self.assertEqual(len(commentaries), 1)

        # Test GET request to retrieve a specific commentary
        commentary_id = commentaries[0]['commentary_id']
        response = self.app.get(f'/commentaries/{commentary_id}')
        self.assertEqual(response.status_code, 200)

        # Test PUT request to update a commentary
        response = self.app.put(f'/commentaries/{commentary_id}', json={"author": "Updated Author"})
        self.assertEqual(response.status_code, 200)
        updated_commentary = response.get_json().get("commentary")
        self.assertEqual(updated_commentary['author'], "Updated Author")

        # Test DELETE request to delete a commentary
        response = self.app.delete(f'/commentaries/{commentary_id}')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()