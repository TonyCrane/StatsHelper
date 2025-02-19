import json
import os
import re
from typing import Optional, Dict
from urllib.request import urlopen

from stats_helper import constants
from stats_helper.config import Config


def name_to_uuid_fromAPI(name):
	url = 'http://tools.glowingmines.eu/convertor/nick/' + name
	js = json.loads(urlopen(url).read().decode('utf8'))
	return js['offlinesplitteduuid']


def isBot(name: str):
	if len(name) < 4 or len(name) > 16:
		return True
	for bad_pattern in Config.get_instance().player_name_blacklist:
		if re.fullmatch(bad_pattern, name, re.IGNORECASE):
			return True
	return False


def get_stat_data(uuid: str, cls: str, target: str) -> Optional[int]:
	try:
		with open(os.path.join(Config.get_instance().get_world_path(), 'stats', uuid + '.json'), 'r') as f:
			cls_name = "minecraft:" + cls if ":" not in cls else cls
			target_data: Dict[str, int] = json.load(f)['stats'][cls_name]
			if target == constants.AllTargetTag:
				return sum(target_data.values())
			target_name = "minecraft:" + target if ":" not in target else target
			return target_data[target_name]
	except:
		return None


def get_rank_color(rank: int) -> str:
	"""
	rank starts from 0
	"""
	return constants.rankColor[min(rank, len(constants.rankColor) - 1)]
