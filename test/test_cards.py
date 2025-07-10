from fastapi import status

from src.infrastructure.logging.logger import log


class TestCardsCRUD:
    def test_create_card(self, test_app, test_db, card_data):
        """Test creating a new card"""
        response = test_app.post("/card/", json=card_data)
        # Check response status code and data
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == card_data["title"]
        assert data["user_id"] == card_data["user_id"]

        # Verify card was created in the database
        card_in_db = test_db["cards"].find_one({"id": data["id"]})
        assert card_in_db is not None
        assert card_in_db["title"] == card_data["title"]
        assert card_in_db["user_id"] == card_data["user_id"]

    def test_list_cards(self, test_app, test_db, card_data, user_data):
        """Test listing cards for a user"""
        # Insert a user and card directly into the database
        log.info('test_list_cards', card_data=card_data, user_data=user_data)
        test_db["users"].insert_one(user_data)
        test_db["cards"].insert_one(card_data)

        # Test listing cards for a user
        response = test_app.get(f"/user/list_cards/{card_data['user_id']}")

        # Check response status code and data
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

        # Verify the inserted card is in the response
        if len(data) > 0:
            card_ids = [card["id"] for card in data]
            assert str(card_data["id"]) in card_ids

    def test_find_card(self, test_app, test_db, card_data):
        """Test finding a card by ID"""
        # Insert a card directly into the database
        test_db["cards"].insert_one(card_data)

        # Test finding a card by ID
        response = test_app.get(f"/card/{card_data['id']}")

        # Check response status code and data
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == str(card_data["id"])
        assert data["title"] == card_data["title"]
        assert data["user_id"] == card_data["user_id"]

    def test_find_card_not_found(self, test_app):
        """Test finding a non-existent card"""
        non_existent_id = "000000000000000000000000"  # Valid ObjectId format
        response = test_app.get(f"/card/{non_existent_id}")

        # Check response status code
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_card(self, test_app, test_db, card_data):
        """Test updating a card"""
        # Insert a card directly into the database
        test_db["cards"].insert_one(card_data)

        # Updated card data
        updated_data = {
            "id": str(card_data["id"]),
            "user_id": card_data["user_id"],
            "title": "Updated Card Title"
        }

        # Test updating a card
        response = test_app.put(f"/card/{card_data['id']}", json=updated_data)

        # Check response status code
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify card was updated in the database
        card_in_db = test_db["cards"].find_one({"id": card_data["id"]})
        log.info('test_update_card', card_in_db=card_in_db)
        assert card_in_db is not None
        assert card_in_db["title"] == updated_data["title"]
        assert card_in_db["user_id"] == updated_data["user_id"]

    def test_update_card_not_found(self, test_app, card_data):
        """Test updating a non-existent card"""
        non_existent_id = "000000000000000000000000"  # Valid ObjectId format

        # Updated card data
        updated_data = {
            "id": non_existent_id,
            "user_id": card_data["user_id"],
            "title": "Updated Card Title"
        }

        response = test_app.put(f"/card/{non_existent_id}", json=updated_data)

        # Check response status code
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_card(self, test_app, test_db, card_data):
        """Test deleting a card"""
        # Insert a card directly into the database
        test_db["cards"].insert_one(card_data)

        # Test deleting a card
        response = test_app.delete(f"/card/{card_data['id']}")

        # Check response status code
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify card was deleted from the database
        card_in_db = test_db["cards"].find_one({"id": card_data["id"]})
        assert card_in_db is None

    def test_delete_card_not_found(self, test_app):
        """Test deleting a non-existent card"""
        non_existent_id = "000000000000000000000000"  # Valid ObjectId format
        response = test_app.delete(f"/card/{non_existent_id}")

        # Check response status code
        assert response.status_code == status.HTTP_404_NOT_FOUND
