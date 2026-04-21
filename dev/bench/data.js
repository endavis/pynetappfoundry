window.BENCHMARK_DATA = {
  "lastUpdate": 1776735817474,
  "repoUrl": "https://github.com/endavis/pynetappfoundry",
  "entries": {
    "Benchmark": [
      {
        "commit": {
          "author": {
            "email": "6662995+endavis@users.noreply.github.com",
            "name": "Eric Davis",
            "username": "endavis"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "0dfdf9cb3b309ddcf6b3e892f3417628cffcd8dc",
          "message": "fix: untrack _version.py so builds produce PyPI-compliant versions (merges PR #662, addresses #661)\n\n_version.py's own header says \"don't change, don't track in version\ncontrol\", but the file was committed long ago. .gitignore already lists\n**/_version.py but gitignore has no effect on tracked files. At build\ntime hatch-vcs overwrites _version.py with the computed version; git\nsees it as modified; setuptools-scm flags the tree dirty and appends a\n+d<date> local-version suffix to the wheel. PyPI and TestPyPI reject\nlocal-version strings with HTTP 400.\n\ngit rm --cached src/pynetappfoundry/_version.py untracks the file. It\nstays on disk, hatch-vcs keeps overwriting it, and setuptools-scm stops\nflagging the tree as dirty. Regression test asserts the file stays\nuntracked via git ls-files --error-unmatch.\n\nAlso removes the now-obsolete\n\"git update-index --assume-unchanged src/pynetappfoundry/_version.py\"\nstep from task_install_dev. That was a workaround for the tracked-file\nproblem this PR fixes at the root; after untracking, the command itself\nfails on untracked files and would break doit install_dev for every\ndeveloper on a fresh clone. Syncs the matching doc entry.\n\nAddresses #661.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T02:42:25+01:00",
          "tree_id": "fe42e4a58a34369a3267ec9171b142b5d88efcb9",
          "url": "https://github.com/endavis/pynetappfoundry/commit/0dfdf9cb3b309ddcf6b3e892f3417628cffcd8dc"
        },
        "date": 1776735816650,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 817831.780326593,
            "unit": "iter/sec",
            "range": "stddev: 2.8433701921816313e-7",
            "extra": "mean: 1.2227453420808128 usec\nrounds: 52062"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 547314.09943874,
            "unit": "iter/sec",
            "range": "stddev: 3.202682495704069e-7",
            "extra": "mean: 1.8271044013400723 usec\nrounds: 127211"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 369235.9075274643,
            "unit": "iter/sec",
            "range": "stddev: 3.8688853168495596e-7",
            "extra": "mean: 2.7082956440947403 usec\nrounds: 125898"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 367956.44987936824,
            "unit": "iter/sec",
            "range": "stddev: 3.6515631029392936e-7",
            "extra": "mean: 2.7177129258852304 usec\nrounds: 134157"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 379760.2723399851,
            "unit": "iter/sec",
            "range": "stddev: 3.922578412372077e-7",
            "extra": "mean: 2.6332401592148047 usec\nrounds: 66077"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 122398.69632446734,
            "unit": "iter/sec",
            "range": "stddev: 6.647920620521164e-7",
            "extra": "mean: 8.170021658965181 usec\nrounds: 46909"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 109771.09536941988,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013511742985511307",
            "extra": "mean: 9.109866277954449 usec\nrounds: 57627"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 59773.919615296756,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012034304115333047",
            "extra": "mean: 16.72970429973426 usec\nrounds: 35979"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 184075.8495070622,
            "unit": "iter/sec",
            "range": "stddev: 6.187849380885857e-7",
            "extra": "mean: 5.432543175424184 usec\nrounds: 37614"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 25919.859469623356,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019849069681600106",
            "extra": "mean: 38.58045608510898 usec\nrounds: 2539"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 72.11831544635908,
            "unit": "iter/sec",
            "range": "stddev: 0.0003368080527318343",
            "extra": "mean: 13.866103136363337 msec\nrounds: 66"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 70.30113402117216,
            "unit": "iter/sec",
            "range": "stddev: 0.00037136867633723205",
            "extra": "mean: 14.224521608696044 msec\nrounds: 69"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 82.89679498350766,
            "unit": "iter/sec",
            "range": "stddev: 0.00019370670721669458",
            "extra": "mean: 12.063192554054114 msec\nrounds: 74"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 13.46581352068593,
            "unit": "iter/sec",
            "range": "stddev: 0.00023569762583162498",
            "extra": "mean: 74.26213042857148 msec\nrounds: 14"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 269.8788898185196,
            "unit": "iter/sec",
            "range": "stddev: 0.00008487429149384485",
            "extra": "mean: 3.7053657685951324 msec\nrounds: 242"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 73.70840331295943,
            "unit": "iter/sec",
            "range": "stddev: 0.0005155142646240456",
            "extra": "mean: 13.566974117646906 msec\nrounds: 68"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.4036668498368576,
            "unit": "iter/sec",
            "range": "stddev: 0.10838486455096619",
            "extra": "mean: 712.4197598000023 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.411295752427231,
            "unit": "iter/sec",
            "range": "stddev: 0.10484130850809556",
            "extra": "mean: 708.5687024000038 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 313628.91891082196,
            "unit": "iter/sec",
            "range": "stddev: 3.743138695955583e-7",
            "extra": "mean: 3.188481481468048 usec\nrounds: 12015"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 303650.4198478457,
            "unit": "iter/sec",
            "range": "stddev: 8.535002018350021e-7",
            "extra": "mean: 3.293260719023816 usec\nrounds: 53130"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 299263.894645733,
            "unit": "iter/sec",
            "range": "stddev: 3.780899769404011e-7",
            "extra": "mean: 3.3415323996360953 usec\nrounds: 49908"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 142228.6763333245,
            "unit": "iter/sec",
            "range": "stddev: 5.908756385414813e-7",
            "extra": "mean: 7.030930933058947 usec\nrounds: 37413"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 163255.14008453864,
            "unit": "iter/sec",
            "range": "stddev: 6.379444334445284e-7",
            "extra": "mean: 6.125381409015168 usec\nrounds: 48077"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 327160.535672127,
            "unit": "iter/sec",
            "range": "stddev: 7.633102036630442e-7",
            "extra": "mean: 3.056603382634689 usec\nrounds: 70892"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 333549.84670184064,
            "unit": "iter/sec",
            "range": "stddev: 3.6097460887030943e-7",
            "extra": "mean: 2.9980526445688866 usec\nrounds: 64793"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 27720.893568818417,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015621558332237065",
            "extra": "mean: 36.07387321470908 usec\nrounds: 14284"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 406800.73074536707,
            "unit": "iter/sec",
            "range": "stddev: 3.244069164912339e-7",
            "extra": "mean: 2.4582060070731293 usec\nrounds: 51406"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 185948.31271446368,
            "unit": "iter/sec",
            "range": "stddev: 9.492069887655388e-7",
            "extra": "mean: 5.377838526212218 usec\nrounds: 48175"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 272804.35597171413,
            "unit": "iter/sec",
            "range": "stddev: 4.452519376855242e-7",
            "extra": "mean: 3.6656306180964555 usec\nrounds: 54556"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 165884.0124318541,
            "unit": "iter/sec",
            "range": "stddev: 5.312985481262251e-7",
            "extra": "mean: 6.028308486996627 usec\nrounds: 42783"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 153863.34151470865,
            "unit": "iter/sec",
            "range": "stddev: 6.512913927356407e-7",
            "extra": "mean: 6.499273902123102 usec\nrounds: 54242"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 38770.27688465584,
            "unit": "iter/sec",
            "range": "stddev: 0.000001329090881282758",
            "extra": "mean: 25.792954818844 usec\nrounds: 19123"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 19669.6607898336,
            "unit": "iter/sec",
            "range": "stddev: 0.000043804713729612144",
            "extra": "mean: 50.83971760798523 usec\nrounds: 9632"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 28104.14545765751,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020014529095168303",
            "extra": "mean: 35.58193937996186 usec\nrounds: 8611"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 270.5616865816428,
            "unit": "iter/sec",
            "range": "stddev: 0.000034770346719490853",
            "extra": "mean: 3.696014807692467 msec\nrounds: 260"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 26.53807988004534,
            "unit": "iter/sec",
            "range": "stddev: 0.0001911626524602972",
            "extra": "mean: 37.68170133333292 msec\nrounds: 27"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 22867.10279702159,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019358264763266685",
            "extra": "mean: 43.7309443560226 usec\nrounds: 13820"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 179.66395336156287,
            "unit": "iter/sec",
            "range": "stddev: 0.011367628627081265",
            "extra": "mean: 5.565946765000547 msec\nrounds: 200"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 13.495944165119615,
            "unit": "iter/sec",
            "range": "stddev: 0.05882911404905541",
            "extra": "mean: 74.09633500000012 msec\nrounds: 20"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 11937.94451664516,
            "unit": "iter/sec",
            "range": "stddev: 0.000003358892506270275",
            "extra": "mean: 83.76651429445772 usec\nrounds: 6436"
          }
        ]
      }
    ]
  }
}