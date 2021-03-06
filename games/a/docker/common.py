"""Base classes and utilities to build Docker agents
"""

import abc
import logging
import pickle
from flask import jsonify

from flask import Flask, request

logger = logging.getLogger(__name__)

class DockerAgent(metaclass=abc.ABCMeta):
    """Abstract base class to implement Docker-based agent"""

    def __init__(self):
        pass

    @abc.abstractmethod
    def act(self, observation, action_space):
        """Given an observation, returns the action the agent should"""
        raise NotImplementedError()

    def run(self, host="0.0.0.0", port=10080):
        """Runs the agent. This creates a webserver that handles incoming action
        requests"""
        app = Flask(self.__class__.__name__)
        @app.route("/action", methods=["POST"])
        def action(): #pylint: disable=W0612
            data = request.get_json()
            observation = data.get("obs")
            observation = pickle.loads(observation.encode("utf-8"))
            action_space = data.get("action_space")
            action_space = pickle.loads(action_space.encode("utf-8"))            
            action = self.act(observation, action_space)
            return jsonify({"action": action})
        
        logger.info("Starting agent server on port %d", port)
        app.run(host=host, port=port)



    


