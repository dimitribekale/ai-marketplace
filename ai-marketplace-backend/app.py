import logging
from flask import Flask, jsonify, request
import blockchain_service
import config  

app = Flask(__name__)


@app.route("/health")
def health_check():
    """A simple health check endpoint."""
    logging.info("Health check endpoint was pinged.")
    return jsonify({"status": "ok", "connected": config.w3.is_connected()})

@app.route("/model-count")
def get_model_count():
    """
    Gets the current model count from the blockchain.
    """
    logging.info("GET /model-count: Request received")
    try:
        # Call the service layer
        count = blockchain_service.get_model_count_from_chain()
        return jsonify({"status": "success", "modelCount": count})
    except Exception as e:
        logging.error(f"Error in /model-count endpoint: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/list-model", methods=["POST"])
def list_model():
    """
    Lists a new model. Expects a JSON body with:
    { "name": "My Model", "price": 1000, "url": "http://..." }
    """
    logging.info("POST /list-model: Request received")
    try:
        data = request.get_json()
        if not data or "name" not in data or "price" not in data or "url" not in data:
            return jsonify({"status": "error", "message": "Missing 'name', 'price', or 'url'"}), 400

        # Call the service layer
        receipt = blockchain_service.list_new_model(
            name=data["name"],
            price=int(data["price"]),
            url=data["url"]
        )
        
        return jsonify({
            "status": "success",
            "message": "Model listed successfully",
            "receipt": receipt
        }), 201

    except Exception as e:
        logging.error(f"Error in /list-model endpoint: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    logging.info(f"Starting Flask server on http://127.0.0.1:5002")
    app.run(debug=True, port=5002)