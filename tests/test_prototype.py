import unittest
from engine.prototype import Graph, workbench

class TestConcept(unittest.TestCase):
    def test_free_build(self):
        g=Graph(); g.add('a','pipe28',600); g.add('b','pipe28',900); g.connect('a','b')
        self.assertEqual(g.joints,[('a','b')]); self.assertEqual(sum(x['qty'] for x in g.bom()),2)
    def test_configure(self):
        a,b=workbench(),workbench(1800)
        self.assertEqual(b.parts['rail0']['length_mm']-a.parts['rail0']['length_mm'],300)
        self.assertEqual(a.parts['leg0'],b.parts['leg0'])
        self.assertEqual(a.joints,b.joints)
    def test_module_remove(self):
        g=workbench(tool_panel=True); g.remove_module('tool_panel')
        self.assertEqual(g.snapshot(),workbench().snapshot())
    def test_mixed(self):
        g=workbench(); g.add('custom','alu40',300,'custom'); g.connect('custom','leg0')
        self.assertIn(('custom','leg0'),g.joints); self.assertEqual(len(g.parts),10)
    def test_invalid(self):
        g=Graph(); g.add('a','pipe28',600); g.add('b','alu40',600)
        with self.assertRaises(ValueError): g.connect('a','b')
        self.assertEqual(g.joints,[])
    def test_repeatable(self):
        self.assertEqual(workbench(1800,tool_panel=True).snapshot(),workbench(1800,tool_panel=True).snapshot())
        self.assertEqual(workbench().snapshot()['engineering_status'],'NEEDS_REVIEW')
