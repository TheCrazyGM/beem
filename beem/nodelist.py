# -*- coding: utf-8 -*-
import re
import time
import math
from timeit import default_timer as timer
import json
from beem.instance import shared_blockchain_instance
from beem.account import Account
import logging

log = logging.getLogger(__name__)


def node_answer_time(node):
    try:
        from beem.blockchaininstance import BlockChainInstance

        stm_local = BlockChainInstance(
            node=node, num_retries=2, num_retries_call=2, timeout=10
        )
        start = timer()
        stm_local.get_network(use_stored_data=False)
        stop = timer()
        rpc_answer_time = stop - start
    except KeyboardInterrupt:
        rpc_answer_time = float("inf")
        raise KeyboardInterrupt()
    except:
        rpc_answer_time = float("inf")
    return rpc_answer_time


class NodeList(list):
    """Returns HIVE/STEEM nodes as list

    .. code-block:: python

        from beem.nodelist import NodeList
        n = NodeList()
        nodes_urls = n.get_nodes()

    """

    def __init__(self):
        nodes = [
            {
                "url": "https://api.steemit.com",
                "version": "0.20.2",
                "type": "appbase",
                "owner": "steemit",
                "hive": False,
                "score": 50,
            },
            {
                "url": "https://api.justyy.com",
                "version": "0.20.2",
                "type": "appbase",
                "owner": "justyy",
                "hive": False,
                "score": 20,
            },
            {
                "url": "https://api.steemdb.online",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "steem_supporter",
                "hive": False,
                "score": 20,
            },
            {
                "url": "https://api.steem.buzz",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "ericet",
                "hive": False,
                "score": 20,
            },
            {
                "url": "https://api.steem.buzz",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "ericet",
                "hive": False,
                "score": 20,
            },
            {
                "url": "https://anyx.io",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "anyx",
                "hive": True,
                "score": 50,
            },
            {
                "url": "https://hive-test-beeabode.roelandp.nl",
                "version": "0.23.0",
                "type": "testnet",
                "owner": "roelandp",
                "hive": True,
                "score": 5,
            },
            {
                "url": "https://api.hivekings.com",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "drakos",
                "hive": True,
                "score": 50,
            },
            {
                "url": "https://api.hive.blog",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "hive",
                "hive": True,
                "score": 80,
            },
            {
                "url": "https://api.openhive.network",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "gtg",
                "hive": True,
                "score": 50,
            },
            {
                "url": "https://techcoderx.com",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "techcoderx",
                "hive": True,
                "score": 10,
            },
            {
                "url": "https://steem.61bts.com",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "ety001",
                "hive": False,
                "score": 10,
            },
            {
                "url": "https://cn.steems.top",
                "version": "0.22.5",
                "type": "appbase",
                "owner": "maiyude",
                "hive": False,
                "score": 10,
            },
            {
                "url": "https://rpc.ecency.com",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "good-karma",
                "hive": True,
                "score": 10,
            },
            {
                "url": "https://hived.privex.io",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "someguy123",
                "hive": True,
                "score": 10,
            },
            {
                "url": "https://api.pharesim.me",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "pharesim",
                "hive": True,
                "score": 10,
            },
            {
                "url": "https://rpc.ausbit.dev",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "ausbitbank",
                "hive": True,
                "score": 50,
            },
            {
                "url": "https://hive.roelandp.nl",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "roelandp",
                "hive": True,
                "score": 50,
            },
            {
                "url": "https://api.c0ff33a.uk",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "c0ff33a",
                "hive": True,
                "score": 40,
            },
            {
                "url": "https://api.deathwing.me",
                "version": "0.23.0",
                "type": "appbase",
                "owner": "deathwing",
                "hive": True,
                "score": 40,
            },
            {
                "url": "https://hive-api.arcange.eu",
                "version": "1.24.2",
                "type": "appbase",
                "owner": "arcange",
                "hive": True,
                "score": 40,
            },
            {
                "url": "https://fin.hive.3speak.co",
                "version": "1.24.2",
                "type": "appbase",
                "owner": "3speak",
                "hive": True,
                "score": 40,
            },
            {
                "url": "https://hived.emre.sh",
                "version": "1.24.2",
                "type": "appbase",
                "owner": "emrebeyler",
                "hive": True,
                "score": 40,
            },
            {
                "url": "https://rpc.mahdiyari.info",
                "version": "1.27.5",
                "type": "appbase",
                "owner": "mahdiyari",
                "hive": True,
                "score": 40,
            },
        ]
        super(NodeList, self).__init__(nodes)

    def update(self, node_list):
        new_nodes = []
        for node_url in node_list:
            node_found = False
            for node in self:
                if node["url"] == node_url:
                    new_nodes.append(node)
                    node_found = True
                    break
            if not node_found:
                log.warning(f"Node {node_url} not found in the original list")

        super(NodeList, self).__init__(new_nodes)

    def get_node_answer_time(self, node_list=None, verbose=False):
        """Pings all nodes and measure the answer time

        .. code-block:: python

            from beem.nodelist import NodeList
            nl = NodeList()
            nl.update_nodes()
            nl.ping_nodes()
        """
        ping_times = []
        if node_list is None:
            node_list = []
            for node in self:
                node_list.append(node["url"])
        for node in node_list:
            ping_times.append(1000.0)
        available_nodes = []
        for node in self:
            available_nodes.append(node["url"])
        for i in range(len(node_list)):
            if node_list[i] not in available_nodes:
                ping_times[i] = float("inf")
                continue
            try:
                ping_times[i] = node_answer_time(node_list[i])
                if verbose:
                    log.info("node %s results in %.2f" % (node_list[i], ping_times[i]))
            except KeyboardInterrupt:
                ping_times[i] = float("inf")
                break
        sorted_arg = sorted(range(len(ping_times)), key=ping_times.__getitem__)
        sorted_nodes = []
        for i in sorted_arg:
            if ping_times[i] != float("inf"):
                sorted_nodes.append(
                    {"url": node_list[i], "delay_ms": ping_times[i] * 1000}
                )
        return sorted_nodes

    def update_nodes(self, weights=None, blockchain_instance=None, **kwargs):
        """Reads metadata from nectarflower and recalculates the nodes score

        :param list/dict weight: can be used to weight the different benchmarks
        :type weight: list, dict

        .. code-block:: python

            from beem.nodelist import NodeList
            nl = NodeList()
            weights = [0, 0.1, 0.2, 1]
            nl.update_nodes(weights)
            weights = {'block': 0.1, 'history': 0.1, 'apicall': 1, 'config': 1}
            nl.update_nodes(weights)
        """
        if blockchain_instance is None:
            if kwargs.get("steem_instance"):
                blockchain_instance = kwargs["steem_instance"]
            elif kwargs.get("hive_instance"):
                blockchain_instance = kwargs["hive_instance"]
        steem = blockchain_instance or shared_blockchain_instance()

        metadata = None
        account = None
        cnt = 0
        while metadata is None and cnt < 5:
            cnt += 1
            try:
                account = Account("nectarflower", blockchain_instance=steem)
                metadata = json.loads(account["posting_json_metadata"])
            except Exception as e:
                log.warning(f"Error fetching metadata (attempt {cnt}): {str(e)}")
                steem.rpc.next()
                account = None
                metadata = None

        if metadata is None:
            log.warning("Failed to fetch nectarflower metadata after multiple attempts")
            return

        report = metadata.get("report", [])
        failing_nodes = metadata.get("failing_nodes", {})
        parameter = metadata.get("parameter", {})
        benchmarks = parameter.get("benchmarks", {})

        # Convert benchmarks dict to list of benchmark names
        benchmark_names = list(benchmarks.keys())

        if weights is None:
            weights_dict = {}
            for benchmark in benchmark_names:
                weights_dict[benchmark] = 1.0 / len(benchmark_names)
        elif isinstance(weights, list):
            weights_dict = {}
            i = 0
            weight_sum = sum(weights)
            for benchmark in benchmark_names:
                if i < len(weights):
                    weights_dict[benchmark] = (
                        weights[i] / weight_sum if weight_sum > 0 else 0
                    )
                else:
                    weights_dict[benchmark] = 0.0
                i += 1
        elif isinstance(weights, dict):
            weights_dict = {}
            weight_sum = sum(weights.values())
            for benchmark in benchmark_names:
                if benchmark in weights:
                    weights_dict[benchmark] = (
                        weights[benchmark] / weight_sum if weight_sum > 0 else 0
                    )
                else:
                    weights_dict[benchmark] = 0.0

        max_score = len(report) + 1
        new_nodes = []
        update_count = 0
        failing_count = 0

        for node in self:
            new_node = node.copy()

            # Check against report data
            for report_node in report:
                if node["url"] == report_node.get("node", ""):
                    update_count += 1
                    new_node["version"] = report_node.get(
                        "version", new_node.get("version", "0.0.0")
                    )
                    new_node["hive"] = report_node.get(
                        "hive", new_node.get("hive", False)
                    )

                    scores = []
                    for benchmark in benchmark_names:
                        if benchmark in report_node:
                            result = report_node[benchmark]
                            rank = result.get("rank", -1)
                            if not result.get("ok", False):
                                rank = max_score + 1
                            score = (
                                (max_score - rank) / (max_score - 1) * 100
                                if rank > 0 and max_score > 1
                                else 0
                            )
                            weighted_score = score * weights_dict.get(benchmark, 0)
                            scores.append(weighted_score)

                    sum_score = sum(scores)
                    new_node["score"] = sum_score
                    break

            # Check if node is in failing nodes list
            if node["url"] in failing_nodes:
                failing_count += 1
                new_node["score"] = -1

            new_nodes.append(new_node)

        super(NodeList, self).__init__(new_nodes)

    def get_nodes(
        self,
        hive=False,
        exclude_limited=False,
        dev=False,
        testnet=False,
        testnetdev=False,
        wss=True,
        https=True,
        not_working=False,
        normal=True,
        appbase=True,
    ):
        """Returns nodes as list

        :param bool hive: When True, only HIVE nodes will be returned
        :param bool exclude_limited: When True, limited nodes are excluded
        :param bool dev: when True, dev nodes with version 0.19.11 are included
        :param bool testnet: when True, testnet nodes are included
        :param bool testnetdev: When True, testnet-dev nodes are included
        :param bool not_working: When True, all nodes including not working ones will be returned
        :param bool normal: deprecated
        :param bool appbase: deprecated

        """
        node_list = []
        node_type_list = []
        if normal:
            node_type_list.append("normal")
        if appbase:
            node_type_list.append("appbase")
        if dev:
            node_type_list.append("appbase-dev")
        if testnet:
            node_type_list.append("testnet")
        if testnetdev:
            node_type_list.append("testnet-dev")
        if not exclude_limited:
            node_type_list.append("appbase-limited")
        for node in self:
            if node["type"] in node_type_list and (node["score"] >= 0 or not_working):
                if hive != node["hive"]:
                    continue
                if not https and node["url"][:5] == "https":
                    continue
                if not wss and node["url"][:3] == "wss":
                    continue
                node_list.append(node)

        return [
            node["url"]
            for node in sorted(node_list, key=lambda self: self["score"], reverse=True)
        ]

    def get_hive_nodes(self, testnet=False, not_working=False, wss=True, https=True):
        """Returns hive only nodes as list

        :param bool testnet: when True, testnet nodes are included
        :param bool not_working: When True, all nodes including not working ones will be returned

        """
        node_list = []
        node_type_list = []

        for node in self:
            if not node["hive"]:
                continue
            if node["score"] < 0 and not not_working:
                continue
            if (testnet and node["type"] == "testnet") or (
                not testnet and node["type"] != "testnet"
            ):
                if not https and node["url"][:5] == "https":
                    continue
                if not wss and node["url"][:3] == "wss":
                    continue
                node_list.append(node)

        return [
            node["url"]
            for node in sorted(node_list, key=lambda self: self["score"], reverse=True)
        ]

    def get_steem_nodes(self, testnet=False, not_working=False, wss=True, https=True):
        """Returns steem only nodes as list

        :param bool testnet: when True, testnet nodes are included
        :param bool not_working: When True, all nodes including not working ones will be returned

        """
        node_list = []
        node_type_list = []

        for node in self:
            if node["hive"]:
                continue
            if node["score"] < 0 and not not_working:
                continue
            if (testnet and node["type"] == "testnet") or (
                not testnet and node["type"] != "testnet"
            ):
                if not https and node["url"][:5] == "https":
                    continue
                if not wss and node["url"][:3] == "wss":
                    continue
                node_list.append(node)

        return [
            node["url"]
            for node in sorted(node_list, key=lambda self: self["score"], reverse=True)
        ]

    def get_testnet(self, testnet=True, testnetdev=False):
        """Returns testnet nodes"""
        return self.get_nodes(
            normal=False, appbase=False, testnet=testnet, testnetdev=testnetdev
        )
