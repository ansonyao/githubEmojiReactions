from fetchData import getReactions
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

result = getReactions('denoland', 'deno')
pp.pprint(result)