from day006 import build_tree, count_orbits, ancest_tree, nearest_common_ancestor, hops_between_two_nodes


def test1():
  sample = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']
  base, node_map = build_tree(sample)
  assert count_orbits(base) == 42
  assert ancest_tree(node_map['K']) == ('K', 'J', 'E', 'D', 'C', 'B', 'COM')
  assert ancest_tree(node_map['I']) == ('I', 'D', 'C', 'B', 'COM')
  assert nearest_common_ancestor(('K', 'J', 'E', 'D', 'C', 'B', 'COM'), ('I', 'D', 'C', 'B', 'COM')) == 'D'
  assert hops_between_two_nodes(node_map, 'K', 'I') == 4
