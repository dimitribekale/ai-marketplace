import { describe, it } from "node:test"; 
import { expect } from "chai";
import hre from "hardhat";
import { parseEther } from "viem";

describe("Marketplace", function () {
  
  // 1. --- The Fixture ---
  // The fixture now gets the 'connection' object automatically
  // when 'loadFixture' calls it.
  async function deployMarketplaceFixture(connection) {
    // Get the connection object from hre
    const [owner, buyer] = await connection.viem.getWalletClients();
    const marketplace = await connection.viem.deployContract("Marketplace");

    const testModel = {
      name: "Test Model",
      price: parseEther("1"), 
      encryptedDownloadUrl: "http://example.com/encrypted-url",
    };

    // Return everything, including the connection for the tests
    return { marketplace, owner, buyer, testModel, connection };
  }

  // 2. --- The First Test ---
  it("Should deploy and have a modelCount of 0", async function () {
    // Get the network helpers from the hre
    const { networkHelpers } = await hre.network.connect();
    
    // Call loadFixture. It will run the fixture function above.
    const { marketplace } = await networkHelpers.loadFixture(deployMarketplaceFixture);

    const count = await marketplace.read.modelCount();
    expect(count).to.equal(0n);
  });


  it("Should allow a seller to list a new model", async function () {
    // Load the fixture
    const { networkHelpers } = await hre.network.connect();
    const { marketplace, owner, testModel } = await networkHelpers.loadFixture(
        deployMarketplaceFixture
    );

    // 1. Call the listModel function
    // We use 'write' because this is a transaction that changes state
    await marketplace.write.listModel(
        [testModel.name, testModel.price, testModel.encryptedDownloadUrl],
        {
            account: owner.account, // Specify WHO is calling this function
        }
    );

    // 2. Check the state changes
    // a. modelCount incrementation
    const newCount = await marketplace.read.modelCount();
    expect(newCount).to.equal(1n);

    // b. model saved or not
    // Call the public 'models' mapping with the ID '1n'
    // Note: viem returns struct data as an array [id, name, price, seller, url]
    const listedModel = await marketplace.read.models([1n]);

    expect(listedModel[0]).to.equal(1n);
    expect(listedModel[1]).to.equal(testModel.name);
    expect(listedModel[2]).to.equal(testModel.price);
    expect(listedModel[3].toLowerCase()).to.equal(owner.account.address.toLowerCase());
  });

  it("Should allow a buyer to purchase a model", async function () {
    // Arrange
    const { networkHelpers, viem } = await hre.network.connect();
    const { marketplace, owner, buyer, testModel } = 
    await networkHelpers.loadFixture(deployMarketplaceFixture);

    // Get the public client to check balances
    const publicClient = await viem.getPublicClient();

    // List the model as the owner
    await marketplace.write.listModel(
        [testModel.name, testModel.price, testModel.encryptedDownloadUrl],
        { account: owner.account}
    );

    // Get the seller's (owner's) balance BEFORE the sale
    const sellerBalanceBefore = await publicClient.getBalance({
        address: owner.account.address,
    });

    // Act
    await marketplace.write.buyModel([1n], {
        account: buyer.account,
        value: testModel.price,
    });

    // Assert
    const sellerBalanceAfter = await publicClient.getBalance(
        {
            address: owner.account.address,
        }
    );
    expect(sellerBalanceAfter).to.equal(sellerBalanceBefore + testModel.price);
  });

});