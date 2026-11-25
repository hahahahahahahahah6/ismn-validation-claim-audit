import tempfile
import unittest
from pathlib import Path
from ismn_validation_claim_audit.audit import audit, claims, evidence
from ismn_validation_claim_audit.phrases import ISMNVALIDATION, NOISMNVALIDATION, GENERIC_NAMES


class AuditTests(unittest.TestCase):
    def test_phrases(self):
        self.assertEqual((len(set(ISMNVALIDATION)), len(set(NOISMNVALIDATION)), len(set(GENERIC_NAMES))), (50, 24, 24))
        for phrase in ISMNVALIDATION:
            with self.subTest(phrase=phrase): self.assertTrue(claims(phrase)[0])
        for phrase in NOISMNVALIDATION:
            with self.subTest(phrase=phrase): self.assertEqual(claims(phrase), (False, True))
        self.assertEqual(claims('```\nvalidate ismn\n```'), (False, False))

    def test_library_routes(self):
        for method in ('validate', 'is_valid', 'ismn_type'):
            for prefix, call in [('import stdnum.ismn', 'stdnum.ismn.' + method), ('import stdnum.ismn as im', 'im.' + method), ('from stdnum import ismn', 'ismn.' + method), ('import stdnum', 'stdnum.ismn.' + method), ('from stdnum.ismn import ' + method, method), ('from stdnum.ismn import ' + method + ' as v', 'v')]:
                with self.subTest(method=method, call=call): self.assertTrue(evidence(prefix + '\n' + call + '(x)'))

    def test_generic_routes(self):
        for name in GENERIC_NAMES:
            for source in ('obj.' + name + '(x)', 'from lib import ' + name + ' as f\nf(x)', 'obj = factory()\nobj.' + name + '(x)'):
                with self.subTest(source=source): self.assertTrue(evidence(source))

    def test_not_evidence(self):
        cases = ['import stdnum.ismn', 'validate(x)', 'is_valid(x)', 'ismn_type(x)', 'validate_ismn(x)', 'obj.validate(x)', 'obj.ismn(x)', 'import stdnum.ismn\nstdnum.ismn.compact(x)', 'import stdnum.ismn\nstdnum.ismn.format(x)', 'import stdnum.ismn\nstdnum.ismn.to_ismn13(x)', 'import stdnum.ismn\nstdnum.ismn.split(x)', 'from stdnum import ean\nean.validate(x)', 'from stdnum import ean\nean.calc_check_digit(x)', 'from stdnum import luhn\nluhn.validate(x)', 'from stdnum import luhn\nluhn.calc_check_digit(x)', 'import re\nre.match(x,y)', 'import re\nre.search(x,y)', 'import re\nre.fullmatch(x,y)', 'len(x) == 13', 'publisher in known', 'validators.ismn(x)', 'lookup.ismn(x)', '"validate ismn"', 'validate_ismn', 'def broken(:', 'import subprocess\nsubprocess.run(["ismn-check"])', 'import stdnum.ismn as im\nim = x\nim.validate(x)', 'from stdnum.ismn import validate\nwith x as validate:\n validate(x)', 'def validate_ismn(x): pass\nobj.validate_ismn(x)']
        cases += ['from stdnum import ' + n + '\n' + n + '.validate(x)' for n in ('isbn', 'issn', 'isan', 'grid')]
        for source in cases:
            with self.subTest(source=source): self.assertFalse(evidence(source))

    def test_findings(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); (p/'README.md').write_text('validate ismn')
            self.assertEqual(audit(p)[0]['severity'], 'HIGH')
            (p/'tests').mkdir(); (p/'tests/test_a.py').write_text('obj.validate_ismn(x)')
            self.assertEqual(audit(p)[0]['severity'], 'MEDIUM')
            (p/'a.py').write_text('obj.validate_ismn(x)')
            self.assertEqual(audit(p), [])
            (p/'README.md').write_text('does not validate ismn')
            self.assertEqual(audit(p)[0]['severity'], 'HIGH')
            (p/'a.py').unlink(); self.assertEqual(audit(p), [])

    def test_exclusions(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); (p/'README.md').write_text('validate ismn')
            for folder in ('fixtures', 'docs', 'examples'):
                (p/folder).mkdir(); (p/folder/'a.py').write_text('obj.validate_ismn(x)')
            (p/'link.py').symlink_to(p/'fixtures/a.py')
            self.assertEqual(audit(p)[0]['severity'], 'HIGH')
            (p/'src.py').write_text('obj.validate_ismn(x)')
            self.assertEqual(audit(p, ['src.py'])[0]['severity'], 'HIGH')
