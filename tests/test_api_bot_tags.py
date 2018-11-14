import json
from tests import SiteTest, app


class ApiBotTagsEndpoint(SiteTest):

    def test_api_tags(self):
        """ Check tag API """

        post_data = json.dumps({
            'tag_name': 'testing',
            'tag_content': 'testing',
            'image_url': None
        })

        get_data = json.dumps({
            'tag_name': 'testing'
        })

        bad_data = json.dumps({
            'not_a_valid_key': 'gross_faceman'
        })

        patch_data = json.dumps({
            'tag_name': 'testing',
            'tag_alias': 'test_alias'
        })

        # POST method - no headers
        response = self.client.post('/bot/tags', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.status_code, 401)

        # POST method - no data
        response = self.client.post('/bot/tags', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 400)

        # POST method - bad data
        response = self.client.post('/bot/tags', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=bad_data)
        self.assertEqual(response.status_code, 400)

        # POST method - save tag
        response = self.client.post('/bot/tags', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True})

        # PATCH method - no headers
        response = self.client.patch('/bot/tags', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.status_code, 401)

        # PATCH method - no data
        response = self.client.patch('/bot/tags', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 400)

        # PATCH method - bad data
        response = self.client.patch('/bot/tags', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'],
                                     data=bad_data)
        self.assertEqual(response.status_code, 400)

        # PATCH method - add alias
        response = self.client.patch('/bot/tags', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'],
                                     data=patch_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True})

        # GET method - no headers
        response = self.client.get('/bot/tags', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.status_code, 401)

        # GET method - get all tags
        response = self.client.get('/bot/tags', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json), list)

        # GET method - get specific tag
        response = self.client.get('/bot/tags?tag_name=testing', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.json, {
            'tag_content': 'testing',
            'tag_name': 'testing',
            'image_url': None
        })
        self.assertEqual(response.status_code, 200)

        # GET method - get from alias
        response = self.client.get('/bot/tags?tag_alias=test_alias', app.config['API_SUBDOMAIN'],
                                   headers=app.config['TEST_HEADER'])
        self.assertEqual(response.json, {
            "tag_alias": "test_alias",
            "tag_name": "testing"
        })
        self.assertEqual(response.status_code, 200)

        # DELETE method - no headers
        response = self.client.delete('/bot/tags', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.status_code, 401)

        # DELETE method - no data
        response = self.client.delete('/bot/tags', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'])
        self.assertEqual(response.status_code, 400)

        # DELETE method - bad data
        response = self.client.delete('/bot/tags', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=bad_data)
        self.assertEqual(response.status_code, 400)

        # DELETE method - delete the testing tag
        response = self.client.delete('/bot/tags', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'], data=get_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True})

        # DELETE method - delete the testing alias
        response = self.client.delete('/bot/tags', app.config['API_SUBDOMAIN'], headers=app.config['TEST_HEADER'],
                                      data=get_data)
        self.assertEqual(response.json, {"success": True})
        self.assertEqual(response.status_code, 200)

