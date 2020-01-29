#!/usr/bin/env python
from __future__ import print_function


def read_file(filename):
  with open(filename, 'r') as file:
    for line in file:
      line = line.rstrip()
      if not line or line[0] == '#':
        continue
      yield line


class Node(object):
  def __init__(self, value, parent=None, children=None):
    self.value = value
    self.parent = parent
    self.children = children if children is not None else []

  def add_child(self, value):
    node = Node(value, parent=self)
    self.children.append(node)
    return node

  def adopt(self, child):
    assert child.is_root
    child.parent = self
    self.children.append(child)

  @property
  def is_root(self):
    return self.parent is None

  @property
  def is_leaf(self):
    return not bool(self.children)


def build_tree(data):
  node_map = {}
  # base = None
  for line in data:
    mass_a, _, mass_b = line.partition(')')
    # if base is None:
    #   base = Node(mass_a)
    #   node_map[mass_a] = base
    if mass_a not in node_map:
      # raise Exception('{} orbits unregistered {}'.format(mass_b, mass_a))
      # puzzle input is out of order! Allow stubs and check later
      node_map[mass_a] = Node(mass_a)
    if mass_b in node_map:
      # Must check for orphans and adopt them
      assert node_map[mass_b].is_root
      node_map[mass_a].adopt(node_map[mass_b])
      continue
    node_map[mass_b] = node_map[mass_a].add_child(mass_b)
  roots = [node for node in node_map.values() if node.is_root]
  if len(roots) > 1:
    raise Exception('Multiple roots: {}'.format(', '.join(n.value for n in roots)))
  base = roots[0]
  return base, node_map


def count_orbits(base):
  def walk(node, results, depth=0):
    results.append(depth)
    for child in node.children:
      walk(child, results, depth + 1)
  results = []
  walk(base, results)
  return sum(results)


def part1_main(filename='day006_input.txt'):
  """Count the number of direct and indirect orbits"""
  base, node_map = build_tree(read_file(filename))
  orbits = count_orbits(base)
  print('Day6, Part1 answer: {}'.format(orbits))


def ancest_tree(node):
  this = node
  path = [this.value]
  while not this.is_root:
    this = this.parent
    path.append(this.value)
  return tuple(path)


def nearest_common_ancestor(path1, path2):
  common = None
  for i in range(1, len(path1)):
    if path1[-i] == path2[-i]:
      common = path1[-i]
    else:
      break
  return common


def hops_between_two_nodes(node_map, node1, node2):
  path1 = ancest_tree(node_map[node1])
  path2 = ancest_tree(node_map[node2])
  common = nearest_common_ancestor(path1, path2)
  return path1.index(common) + path2.index(common)


def part2_main(filename='day006_input.txt'):
  """Find the number of hops between YOU and SAN"""
  # Strat: build tree, find common ancestor, avoid off-by-ones
  base, node_map = build_tree(read_file(filename))
  your_planet = node_map['YOU'].parent.value
  santas_planet = node_map['SAN'].parent.value
  distance = hops_between_two_nodes(node_map, your_planet, santas_planet)
  print('Day6, Part2 answer: {}'.format(distance))


if __name__ == '__main__':
  part1_main()
  part2_main()
