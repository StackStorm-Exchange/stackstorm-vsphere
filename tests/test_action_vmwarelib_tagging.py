from vmwarelib.tagging import VmwareTagging
import logging
import mock
import unittest


class TaggingTestCase(unittest.TestCase):

    def create_class_object(self):
        mock_session = mock.MagicMock()
        tagging = VmwareTagging(server='vsphere.domain.tld',
                                username='user',
                                password='pass',
                                logger=logging.getLogger(__name__))
        tagging.session = mock_session
        return tagging

    def test_init(self):
        action = self.create_class_object()
        self.assertIsInstance(action, VmwareTagging)

    ############################################################################

    # Request Actions

    def test_make_url(self):
        action = self.create_class_object()
        result = action.make_url("/fake/endpoint")
        self.assertEqual(result, "https://vsphere.domain.tld/fake/endpoint")

    def test_get(self):
        # setup
        action = self.create_class_object()
        expected = {"fake": "data",
                    "key": "123"}

        # mock
        mock_response = mock.MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = expected

        mock_session = mock.MagicMock()
        mock_session.get.return_value = mock_response

        action.session = mock_session

        # execute
        result = action.get("/fake/get/endpoint")

        # assert
        action.session.get.assert_called_with("https://vsphere.domain.tld/fake/get/endpoint",
                                              params=None)
        mock_response.raise_for_status.assert_called_with()
        self.assertEqual(result, expected)

    def test_post_payload_with_response(self):
        # setup
        action = self.create_class_object()
        payload = {"my": "payload"}
        expected = {"fake": "data",
                    "key": "123"}

        # mock
        mock_response = mock.MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = expected
        mock_response.text = "abc"

        mock_session = mock.MagicMock()
        mock_session.post.return_value = mock_response

        action.session = mock_session

        # execute
        result = action.post("/fake/post/endpoint", payload)

        # assert
        action.session.post.assert_called_with("https://vsphere.domain.tld/fake/post/endpoint",
                                               json=payload,
                                               params=None)
        mock_response.raise_for_status.assert_called_with()
        self.assertEqual(result, expected)

    def test_post_with_params(self):
        # setup
        action = self.create_class_object()
        payload = {"my": "payload"}
        expected = {"fake": "data",
                    "key": "123"}

        # mock
        mock_response = mock.MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = expected
        mock_response.text = "abc"

        mock_session = mock.MagicMock()
        mock_session.post.return_value = mock_response

        action.session = mock_session

        # execute
        result = action.post("/fake/post/endpoint", payload, params={'abc', '123'})

        # assert
        action.session.post.assert_called_with("https://vsphere.domain.tld/fake/post/endpoint",
                                               json=payload,
                                               params={'abc', '123'})
        mock_response.raise_for_status.assert_called_with()
        self.assertEqual(result, expected)

    def test_post_no_payload_with_no_response(self):
        # setup
        action = self.create_class_object()

        # mock
        mock_response = mock.MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = ""

        mock_session = mock.MagicMock()
        mock_session.post.return_value = mock_response

        action.session = mock_session

        # execute
        result = action.post("/fake/post/endpoint")

        # assert
        action.session.post.assert_called_with("https://vsphere.domain.tld/fake/post/endpoint",
                                               json=None,
                                               params=None)
        mock_response.raise_for_status.assert_called_with()
        self.assertEqual(result, None)

    def test_delete_payload_with_response(self):
        # setup
        action = self.create_class_object()
        payload = {"my": "payload"}
        expected = {"fake": "data",
                    "key": "123"}

        # mock
        mock_response = mock.MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = expected
        mock_response.text = "abc"

        mock_session = mock.MagicMock()
        mock_session.delete.return_value = mock_response

        action.session = mock_session

        # execute
        result = action.delete("/fake/delete/endpoint", payload)

        # assert
        action.session.delete.assert_called_with("https://vsphere.domain.tld/fake/delete/endpoint",
                                                 json=payload,
                                                 params=None)
        mock_response.raise_for_status.assert_called_with()
        self.assertEqual(result, expected)

    def test_delete_no_payload_with_no_response(self):
        # setup
        action = self.create_class_object()

        # mock
        mock_response = mock.MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = ""

        mock_session = mock.MagicMock()
        mock_session.delete.return_value = mock_response

        action.session = mock_session

        # execute
        result = action.delete("/fake/delete/endpoint")

        # assert
        action.session.delete.assert_called_with("https://vsphere.domain.tld/fake/delete/endpoint",
                                                 json=None,
                                                 params=None)
        mock_response.raise_for_status.assert_called_with()
        self.assertEqual(result, None)

    def test_delete_params(self):
        # setup
        action = self.create_class_object()

        # mock
        mock_response = mock.MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = ""

        mock_session = mock.MagicMock()
        mock_session.delete.return_value = mock_response

        action.session = mock_session

        # execute
        result = action.delete("/fake/delete/endpoint", params={'abc': '123'})

        # assert
        action.session.delete.assert_called_with("https://vsphere.domain.tld/fake/delete/endpoint",
                                                 json=None,
                                                 params={'abc': '123'})
        mock_response.raise_for_status.assert_called_with()
        self.assertEqual(result, None)

    ############################################################################

    def test_login(self):
        # setup
        action = self.create_class_object()

        expected = {"fake": "data",
                    "value": "123"}
        expected_string = '{"fake": "data", "value": "123"}'
        expected_cookies = {"auth": "data",
                            "info": "cookie"}
        expected_headers = {'vmware-api-session-id': '123'}

        # mock
        mock_response = mock.MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.cookies = expected_cookies
        mock_response.content = expected_string

        mock_session = mock.MagicMock()
        mock_session.headers = {}
        mock_session.post.return_value = mock_response

        action.session = mock_session

        # execute
        result = action.login()

        # assert
        action.session.post.assert_called_with("https://vsphere.domain.tld/rest/com/vmware/cis/session",
                                               headers={"vmware-use-header-authn": "true"})
        mock_response.raise_for_status.assert_called_with()
        self.assertEqual(result, expected_cookies)
        self.assertEqual(action.session.headers, expected_headers)

    ############################################################################

    # Category Functions

    @mock.patch("vmwarelib.tagging.VmwareTagging.get")
    def test_category_list(self, mock_get):
        # setup
        action = self.create_class_object()
        expected = "expected_value"
        mock_get.return_value = {"value": expected}

        # execute
        result = action.category_list()

        # assert
        mock_get.assert_called_with("/rest/com/vmware/cis/tagging/category")
        self.assertEquals(result, expected)

    @mock.patch("vmwarelib.tagging.VmwareTagging.get")
    def test_category_get(self, mock_get):
        # setup
        action = self.create_class_object()
        category_id = "1234"
        expected = "expected_value"
        mock_get.return_value = {"value": expected}

        # execute
        result = action.category_get(category_id)

        # assert
        mock_get.assert_called_with("/rest/com/vmware/cis/tagging/category/id:1234")
        self.assertEquals(result, expected)

    @mock.patch("vmwarelib.tagging.VmwareTagging.delete")
    def test_category_delete(self, mock_delete):
        # setup
        action = self.create_class_object()
        category_id = "1234"
        expected = "expected_value"
        mock_delete.return_value = expected

        # execute
        result = action.category_delete(category_id)

        # assert
        mock_delete.assert_called_with("/rest/com/vmware/cis/tagging/category/id:1234")
        self.assertEquals(result, expected)

    @mock.patch("vmwarelib.tagging.VmwareTagging.category_get")
    @mock.patch("vmwarelib.tagging.VmwareTagging.category_list")
    def test_category_find_by_name(self, mock_category_list, mock_category_get):
        # setup
        action = self.create_class_object()

        # mock
        mock_category_list.return_value = ["1", "2", "3"]
        mock_category_get.side_effect = [{"name": "a", "value": "x"},
                                         {"name": "b", "value": "xx"},
                                         {"name": "c", "value": "xxx"}]

        # execute
        result = action.category_find_by_name("b")

        # assert
        self.assertEquals(result, {"name": "b", "value": "xx"})

    @mock.patch("vmwarelib.tagging.VmwareTagging.category_get")
    @mock.patch("vmwarelib.tagging.VmwareTagging.category_list")
    def test_category_find_by_name_not_found(self, mock_category_list, mock_category_get):
        # setup
        action = self.create_class_object()

        # mock
        mock_category_list.return_value = ["1", "2", "3"]
        mock_category_get.side_effect = [{"name": "a", "value": "x"},
                                         {"name": "b", "value": "xx"},
                                         {"name": "c", "value": "xxx"}]

        # execute
        result = action.category_find_by_name("abc123")

        # assert
        self.assertEquals(result, None)

    def test_category_create_spec(self):
        action = self.create_class_object()
        create_spec = action.category_create_spec()
        self.assertEquals(create_spec, {"name": "",
                                        "description": "",
                                        "cardinality": "SINGLE",
                                        "associable_types": []})

    @mock.patch("vmwarelib.tagging.VmwareTagging.post")
    def test_category_create_all_params(self, mock_post):
        # setup
        action = self.create_class_object()
        test_name = "category_name"
        test_description = "Category Description"
        test_cardinality = "MULTIPLE"
        test_associable_types = ['VirtualMachine']

        expected_create_spec = {"name": test_name,
                                "description": test_description,
                                "cardinality": test_cardinality,
                                "associable_types": ['VirtualMachine']}

        # mock
        mock_post.return_value = {"value": "expected result"}

        # execute
        print("calling category create from test")
        result = action.category_create(test_name, test_description, test_cardinality,
                                        test_associable_types)

        # assert
        mock_post.assert_called_with("/rest/com/vmware/cis/tagging/category",
                                     payload={"create_spec": expected_create_spec})
        self.assertEquals(result, "expected result")

    @mock.patch("vmwarelib.tagging.VmwareTagging.post")
    def test_category_create_no_params(self, mock_post):
        # setup
        action = self.create_class_object()
        test_name = "category_name"

        expected_create_spec = {"name": test_name,
                                "description": "",
                                "cardinality": "SINGLE",
                                "associable_types": []}

        # mock
        mock_post.return_value = {"value": "expected result"}

        # execute
        result = action.category_create(test_name)

        # assert
        mock_post.assert_called_with("/rest/com/vmware/cis/tagging/category",
                                     payload={"create_spec": expected_create_spec})
        self.assertEquals(result, "expected result")

    @mock.patch("vmwarelib.tagging.VmwareTagging.category_find_by_name")
    def test_category_get_or_create_get(self, mock_category_find_by_name):
        # setup
        action = self.create_class_object()

        # mock
        mock_category_find_by_name.return_value = "fake category"

        # execute
        result = action.category_get_or_create("name")

        # assert
        mock_category_find_by_name.assert_called_with("name")
        self.assertEquals(result, "fake category")

    @mock.patch("vmwarelib.tagging.VmwareTagging.category_get")
    @mock.patch("vmwarelib.tagging.VmwareTagging.category_create")
    @mock.patch("vmwarelib.tagging.VmwareTagging.category_find_by_name")
    def test_category_get_or_create_create_all_params(self, mock_category_find_by_name,
                                                      mock_category_create,
                                                      mock_category_get):
        # setup
        action = self.create_class_object()
        test_name = "category_name"
        test_description = "Category Description"
        test_cardinality = "MULTIPLE"
        test_associable_types = []

        # mock
        mock_category_find_by_name.return_value = None
        mock_category_create.return_value = "123"
        mock_category_get.return_value = "fake category"

        # execute
        result = action.category_get_or_create(test_name, test_description, test_cardinality,
                                               test_associable_types)

        # assert
        mock_category_find_by_name.assert_called_with(test_name)
        mock_category_create.assert_called_with(test_name, test_description, test_cardinality,
                                                test_associable_types)
        mock_category_get.assert_called_with("123")
        self.assertEquals(result, "fake category")

    @mock.patch("vmwarelib.tagging.VmwareTagging.category_get")
    @mock.patch("vmwarelib.tagging.VmwareTagging.category_create")
    @mock.patch("vmwarelib.tagging.VmwareTagging.category_find_by_name")
    def test_category_get_or_create_create_no_params(self, mock_category_find_by_name,
                                                     mock_category_create,
                                                     mock_category_get):
        # setup
        action = self.create_class_object()
        test_name = "category_name"

        # mock
        mock_category_find_by_name.return_value = None
        mock_category_create.return_value = "123"
        mock_category_get.return_value = "fake category"

        # execute
        result = action.category_get_or_create(test_name)

        # assert
        mock_category_find_by_name.assert_called_with(test_name)
        mock_category_create.assert_called_with(test_name, None, None, None)
        mock_category_get.assert_called_with("123")
        self.assertEquals(result, "fake category")

    ############################################################################

    # Tag Functions

    @mock.patch("vmwarelib.tagging.VmwareTagging.post")
    def test_tag_list_category(self, mock_post):
        # setup
        action = self.create_class_object()
        test_category_id = "1234"
        expected = "expected_value"
        mock_post.return_value = {"value": expected}

        # execute
        result = action.tag_list(test_category_id)

        # assert
        mock_post.assert_called_with("/rest/com/vmware/cis/tagging/tag/id:1234",
                                     params={"~action": "list-tags-for-category"})
        self.assertEquals(result, expected)

    @mock.patch("vmwarelib.tagging.VmwareTagging.get")
    def test_tag_list_no_category(self, mock_get):
        # setup
        action = self.create_class_object()
        expected = "expected_value"
        mock_get.return_value = {"value": expected}

        # execute
        result = action.tag_list()

        # assert
        mock_get.assert_called_with("/rest/com/vmware/cis/tagging/tag")
        self.assertEquals(result, expected)

    @mock.patch("vmwarelib.tagging.VmwareTagging.get")
    def test_tag_get(self, mock_get):
        # setup
        action = self.create_class_object()
        tag_id = "1234"
        expected = "expected_value"
        mock_get.return_value = {"value": expected}

        # execute
        result = action.tag_get(tag_id)

        # assert
        mock_get.assert_called_with("/rest/com/vmware/cis/tagging/tag/id:1234")
        self.assertEquals(result, expected)

    @mock.patch("vmwarelib.tagging.VmwareTagging.delete")
    def test_tag_delete(self, mock_delete):
        # setup
        action = self.create_class_object()
        tag_id = "1234"
        expected = "expected_value"
        mock_delete.return_value = expected

        # execute
        result = action.tag_delete(tag_id)

        # assert
        mock_delete.assert_called_with("/rest/com/vmware/cis/tagging/tag/id:1234")
        self.assertEquals(result, expected)

    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_get")
    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_list")
    def test_tag_find_by_name(self, mock_tag_list, mock_tag_get):
        # setup
        action = self.create_class_object()
        test_category_id = "1234"
        test_tag_name = "b"

        # mock
        mock_tag_list.return_value = [1, 2, 3]
        mock_tag_get.side_effect = [{"name": "a", "value": "x"},
                                    {"name": "b", "value": "xx"},
                                    {"name": "c", "value": "xxx"}]

        # execute
        result = action.tag_find_by_name(test_tag_name, test_category_id)

        # assert
        mock_tag_list.assert_called_with(test_category_id)
        self.assertEquals(result, {"name": "b", "value": "xx"})

    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_get")
    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_list")
    def test_tag_find_not_found(self, mock_tag_list, mock_tag_get):
        # setup
        action = self.create_class_object()
        test_tag_list = ["1", "2", "3"]

        # mock
        mock_tag_list.return_value = test_tag_list
        mock_tag_get.side_effect = [{"name": "a", "value": "x"},
                                    {"name": "b", "value": "xx"},
                                    {"name": "c", "value": "xxx"}]

        # execute
        result = action.tag_find_by_name("abc123")

        # assert
        mock_tag_list.assert_called_with(None)
        mock_tag_get.assert_has_calls([mock.call("1"), mock.call("2"), mock.call("3")],
                                      any_order=True)
        self.assertEquals(result, None)

    def test_tag_create_spec(self):
        action = self.create_class_object()
        create_spec = action.tag_create_spec()
        self.assertEquals(create_spec, {"name": "",
                                        "description": "",
                                        "category_id": ""})

    @mock.patch("vmwarelib.tagging.VmwareTagging.post")
    def test_tag_create(self, mock_post):
        # setup
        action = self.create_class_object()
        test_tag_name = "name"
        test_category_id = "1234"
        expected_create_spec = {"name": test_tag_name,
                                "description": "",
                                "category_id": test_category_id}

        # mock
        mock_post.return_value = {"value": "expected result"}

        # execute
        result = action.tag_create(test_tag_name, test_category_id)

        # assert
        mock_post.assert_called_with("/rest/com/vmware/cis/tagging/tag",
                                     payload={"create_spec": expected_create_spec})
        self.assertEquals(result, "expected result")

    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_find_by_name")
    def test_tag_get_or_create_get(self, mock_tag_find_by_name):
        # setup
        action = self.create_class_object()
        test_tag_name = "name"
        test_category_id = "1234"

        # mock
        mock_tag_find_by_name.return_value = "fake tag"

        # execute
        result = action.tag_get_or_create(test_tag_name, test_category_id)

        # assert
        mock_tag_find_by_name.assert_called_with(test_tag_name, test_category_id)
        self.assertEquals(result, "fake tag")

    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_get")
    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_create")
    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_find_by_name")
    def test_tag_get_or_create_create(self, mock_tag_find_by_name,
                                      mock_tag_create,
                                      mock_tag_get):
        action = self.create_class_object()
        test_tag_name = "name"
        test_category_id = "1234"

        mock_tag_find_by_name.return_value = None
        mock_tag_create.return_value = "123"
        mock_tag_get.return_value = "fake tag"

        result = action.tag_get_or_create(test_tag_name, test_category_id)

        mock_tag_find_by_name.assert_called_with(test_tag_name, test_category_id)
        mock_tag_create.assert_called_with(test_tag_name, test_category_id, None)
        mock_tag_get.assert_called_with("123")
        self.assertEquals(result, "fake tag")

    ############################################################################

    # Tag Association Functions

    def test_tag_association_endpoint(self):
        action = self.create_class_object()
        result = action.tag_association_endpoint()
        self.assertEquals(result,
                          "/rest/com/vmware/cis/tagging/tag-association")

    def test_tag_association_endpoint_tag_id(self):
        action = self.create_class_object()
        result = action.tag_association_endpoint("123")
        self.assertEquals(result,
                          "/rest/com/vmware/cis/tagging/tag-association/id:123")

    @mock.patch("vmwarelib.tagging.VmwareTagging.post")
    def test_tag_association_attach(self, mock_post):
        action = self.create_class_object()
        mock_post.return_value = "response"
        result = action.tag_association_attach("123", "vm", "vm-789")

        mock_post.assert_called_with("/rest/com/vmware/cis/tagging/tag-association/id:123",
                                     params={'~action': "attach"},
                                     payload={"object_id": {"id": "vm-789",
                                                            "type": "vm"}})
        self.assertEquals(result, "response")

    @mock.patch("vmwarelib.tagging.VmwareTagging.post")
    def test_tag_association_attach_multiple(self, mock_post):
        action = self.create_class_object()
        test_tag_ids = ["123", "321"]
        mock_post.return_value = "response"
        result = action.tag_association_attach_multiple(test_tag_ids, "vm", "vm-789")

        mock_post.assert_called_with("/rest/com/vmware/cis/tagging/tag-association",
                                     params={'~action': 'attach-multiple-tags-to-object'},
                                     payload={"tag_ids": test_tag_ids,
                                              "object_id": {"id": "vm-789",
                                                            "type": "vm"}})
        self.assertEquals(result, "response")

    @mock.patch("vmwarelib.tagging.VmwareTagging.post")
    def test_tag_association_detach(self, mock_post):
        action = self.create_class_object()
        mock_post.return_value = "response"
        result = action.tag_association_detach("123", "vm", "vm-789")

        mock_post.assert_called_with('/rest/com/vmware/cis/tagging/tag-association/id:123',
                                     params={'~action': 'detach'},
                                     payload={"object_id": {"id": "vm-789",
                                                            "type": "vm"}})
        self.assertEquals(result, "response")

    @mock.patch("vmwarelib.tagging.VmwareTagging.post")
    def test_tag_association_list_attached_tags(self, mock_post):
        action = self.create_class_object()
        mock_post.return_value = {'value': "response"}
        result = action.tag_association_list_attached_tags("vm", "vm-789")

        mock_post.assert_called_with("/rest/com/vmware/cis/tagging/tag-association",
                                     params={'~action': 'list-attached-tags'},
                                     payload={"object_id": {"id": "vm-789",
                                                            "type": "vm"}})
        self.assertEquals(result, "response")

    @mock.patch("vmwarelib.tagging.VmwareTagging.post")
    def test_tag_association_list_attached_objects(self, mock_post):
        action = self.create_class_object()
        mock_post.return_value = {'value': "response"}
        result = action.tag_association_list_attached_objects("123")

        mock_post.assert_called_with("/rest/com/vmware/cis/tagging/tag-association/id:123",
                                     params={'~action': 'list-attached-objects'})
        self.assertEquals(result, "response")

    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_association_detach")
    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_get")
    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_association_list_attached_tags")
    def test_tag_association_detach_category(self, mock_tag_association_list_attached_tags,
                                             mock_tag_get,
                                             mock_tag_association_detach):
        action = self.create_class_object()
        mock_tag_association_list_attached_tags.return_value = ["1", "2", "3"]
        mock_tag_get.side_effect = [{"name": "1", "category_id": "c1"},
                                    {"name": "2", "category_id": "c1"},
                                    {"name": "3", "category_id": "c2"}]

        results = action.tag_association_detach_category("c2", "vm", "vm-123")
        self.assertEquals(results, [{"name": "3", "category_id": "c2"}])

    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_association_detach")
    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_get")
    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_association_list_attached_tags")
    def test_tag_association_detach_category_no_match(self,
                                                      mock_tag_association_list_attached_tags,
                                                      mock_tag_get,
                                                      mock_tag_association_detach):
        action = self.create_class_object()
        mock_tag_association_list_attached_tags.return_value = ["1", "2", "3"]
        mock_tag_get.side_effect = [{"name": "1", "category_id": "c1"},
                                    {"name": "2", "category_id": "c1"},
                                    {"name": "3", "category_id": "c2"}]

        results = action.tag_association_detach_category("xyz", "vm", "vm-123")
        self.assertEquals(results, [])

    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_association_attach")
    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_association_detach_category")
    @mock.patch("vmwarelib.tagging.VmwareTagging.tag_get")
    def test_tag_association_replace(self, mock_tag_get,
                                     mock_tag_association_detach_category,
                                     mock_tag_association_attach):
        action = self.create_class_object()
        mock_tag_get.return_value = {"name": "xyz", "category_id": "567"}

        mock_tag_association_attach.return_value = "expected"
        results = action.tag_association_replace("123", "vm", "vm-789")

        mock_tag_get.assert_called_with("123")
        mock_tag_association_detach_category.assert_called_with("567",
                                                                "vm",
                                                                "vm-789")
        mock_tag_association_attach.assert_called_with("123",
                                                       "vm",
                                                       "vm-789")
        self.assertEquals(results, "expected")
