// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.24;

/**
 * @title AI Model and Data Marketplace
 * @author Dimitri Bekale
 * @notice This contract is the central escrow and logic for a decentralized marketplace.
 */

contract Marketplace {
    // 1. Define the data structure for a Model
    struct Model {
        uint256 id;
        string name;
        uint256 price; // Price in WEI
        address payable seller; // Address of the person selling it
        string encryptedDownloadUrl;
    }

    // 2. Create a "database" to store all the models
    // This maps an ID (uint256) to a model object
    mapping(uint256 => Model) public models;

    // 3. A counter to keep track of how many models we have
    // This will also act as our unique ID generator
    uint256 public modelCount;

    // 4. An "Event" to announce that a new model has been listed
    event ModelListed(
        uint256 id,
        string name,
        uint256 price,
        address indexed seller
    );

    // 5. Function to list a new model
    function listModel(string memory _name, uint256 _price, string memory _encryptedDownloadUrl) public {
        // Increment the counter to get a new, unique ID
        modelCount++;

        // Create the new Model object in memory
        Model memory newModel = Model(
            modelCount,
            _name,
            _price,
            payable(msg.sender), // msg.sender is the person calling the function.
            _encryptedDownloadUrl
        );
        // Save to the "database" (the mapping)
        models[modelCount] = newModel;
        // Announce the event
        emit ModelListed(modelCount, _name, _price, msg.sender);
    }
    // 6. An "Event" to announce that a model has been sold
    event ModelPurchased(
        uint256 indexed id,
        string name,
        uint256 price,
        address indexed seller,
        address indexed buyer

    );

    // 7. Function to buy a model
    function buyModel(uint256 _modelId) public payable {
        // 1. Cheks
        // a. Does the model exist?
        require(_modelId > 0 && _modelId <= modelCount, "Model does not exist");

        // Get the model from storage
        Model storage _model = models[_modelId];

        // b. Check whether the buyer sent enough money
        // 'msg.value' is the amount of crypto sent with the function call
        require(msg.value >= _model.price, "Not enough Ether send; check the price");

        // c. Check whether the buyer is buying their own model
        require(msg.sender != _model.seller, "Seller cannot buy their own model");

        // 2. Effect
        // This part is for transaction history like model marked as sold for example

        // 3. Interactions
        // Sending money is an "interaction" with another address
        // Send money to the seller
        (bool sent, ) = _model.seller.call{value: _model.price}("");
        require(sent, "Failed to transfer Ether to seller");

        // Announce the purchase
        emit ModelPurchased(
            _modelId,
            _model.name,
            _model.price,
            _model.seller,
            msg.sender
        );

    }
}