import { describe, it } from "node:test"; 
import { expect } from "chai";
import hre from "hardhat";
import { parseEther } from "viem";

describe("Marketplace", function () {
  
  // 1. --- The Fixture ---
  // The fixture now gets the 'connection' object automatically
  // when 'loadFixture' calls it.
  async function deployMarketplaceFixture() {
    // Get the connection object from hre
    const connection = await hre.network.connect();
    
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
  })
});