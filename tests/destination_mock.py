from flask import Flask, jsonify, request

app = Flask(__name__)


# Root endpoint to test the base proxy route without a sub-path
@app.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def root_endpoint():
    if request.method == "GET":
        return jsonify({"status": "root accessed", "method": "GET"}), 200
    elif request.method == "POST":
        data = request.get_json()
        return (
            jsonify(
                {"status": "root accessed", "method": "POST", "received_data": data}
            ),
            201,
        )
    elif request.method == "PUT":
        data = request.get_json()
        return (
            jsonify({"status": "root accessed", "method": "PUT", "update_info": data}),
            200,
        )
    elif request.method == "DELETE":
        return (
            jsonify(
                {
                    "status": "root accessed",
                    "method": "DELETE",
                    "message": "Resource deleted",
                }
            ),
            204,
        )


# Simple /health endpoint to return a health status
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "Server is running smoothly"}), 200


# Example POST endpoint to test forwarding of data
@app.route("/data", methods=["POST"])
def receive_data():
    data = request.get_json()
    return jsonify({"status": "success", "received_data": data}), 201


# Example PUT endpoint to test updating resources
@app.route("/update", methods=["PUT"])
def update_resource():
    update_info = request.get_json()
    return jsonify({"status": "updated", "update_info": update_info}), 200


# Example DELETE endpoint to test resource deletion
@app.route("/delete", methods=["DELETE"])
def delete_resource():
    return jsonify({"status": "resource deleted"}), 204


if __name__ == "__main__":
    # Start the Flask app on port 8080 to match the proxy configuration
    app.run(host="0.0.0.0", port=8080)
