from flask import Flask, request, jsonify, render_template
import ipaddress

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ipcalc", methods=["GET"])
def ipcalc():
    ip = request.args.get("host")       # 例如 192.168.0.1
    mask1 = request.args.get("mask1")   # 例如 24
    mask2 = request.args.get("mask2")   # 可選，通常留空

    try:
        # 組合成 CIDR
        network = ipaddress.ip_network(f"{ip}/{mask1}", strict=False)

        result = {
            "network": str(network.network_address),
            "broadcast": str(network.broadcast_address),
            "firstHost": str(list(network.hosts())[0]),
            "lastHost": str(list(network.hosts())[-1]),
            "hostCount": network.num_addresses - 2
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
