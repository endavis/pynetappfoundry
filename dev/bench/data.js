window.BENCHMARK_DATA = {
  "lastUpdate": 1778159433816,
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
      },
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
          "id": "1f8a87909d4336b0661f8ad05374114acdcca2d1",
          "message": "release: v0.1.0a1 (merges PR #663)\n\nchore: update changelog for v0.1.0a1",
          "timestamp": "2026-04-21T02:59:39+01:00",
          "tree_id": "2cd612b2ad41238cef7ee00f5ca29945d58eeabb",
          "url": "https://github.com/endavis/pynetappfoundry/commit/1f8a87909d4336b0661f8ad05374114acdcca2d1"
        },
        "date": 1776736849775,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 833231.824032036,
            "unit": "iter/sec",
            "range": "stddev: 3.3422416916864026e-7",
            "extra": "mean: 1.2001461912015883 usec\nrounds: 43833"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 539882.0605008589,
            "unit": "iter/sec",
            "range": "stddev: 5.455187949715362e-7",
            "extra": "mean: 1.8522563966513 usec\nrounds: 137533"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 367917.0389182615,
            "unit": "iter/sec",
            "range": "stddev: 6.531099748118581e-7",
            "extra": "mean: 2.7180040449884295 usec\nrounds: 130532"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 367170.826978434,
            "unit": "iter/sec",
            "range": "stddev: 6.372254505290235e-7",
            "extra": "mean: 2.7235279235807464 usec\nrounds: 136408"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 359352.25045960664,
            "unit": "iter/sec",
            "range": "stddev: 6.082644951617219e-7",
            "extra": "mean: 2.782784854473608 usec\nrounds: 66792"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 111409.21177695382,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010316065852711395",
            "extra": "mean: 8.975918454589234 usec\nrounds: 24796"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 98555.34402811452,
            "unit": "iter/sec",
            "range": "stddev: 0.000001190477348707193",
            "extra": "mean: 10.146583220436364 usec\nrounds: 55353"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 57873.463326019504,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014759853633555007",
            "extra": "mean: 17.279076497749653 usec\nrounds: 35086"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 173501.75349705567,
            "unit": "iter/sec",
            "range": "stddev: 8.367711026669269e-7",
            "extra": "mean: 5.7636305100338365 usec\nrounds: 37568"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 23613.339450114603,
            "unit": "iter/sec",
            "range": "stddev: 0.000002312708384085329",
            "extra": "mean: 42.34894442239286 usec\nrounds: 2519"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 68.03462791502619,
            "unit": "iter/sec",
            "range": "stddev: 0.0006876927897520766",
            "extra": "mean: 14.698397428570916 msec\nrounds: 56"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 65.8271925418037,
            "unit": "iter/sec",
            "range": "stddev: 0.0010295356784044438",
            "extra": "mean: 15.191290428570957 msec\nrounds: 56"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 76.34927950182504,
            "unit": "iter/sec",
            "range": "stddev: 0.0005429996918521294",
            "extra": "mean: 13.097700548386921 msec\nrounds: 62"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.360250852678472,
            "unit": "iter/sec",
            "range": "stddev: 0.0006579181378255099",
            "extra": "mean: 96.52275936363708 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 268.0175376759549,
            "unit": "iter/sec",
            "range": "stddev: 0.00007031989487940943",
            "extra": "mean: 3.7310991238530242 msec\nrounds: 218"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 68.48637548047272,
            "unit": "iter/sec",
            "range": "stddev: 0.000937893406172922",
            "extra": "mean: 14.60144434545418 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2239686404624996,
            "unit": "iter/sec",
            "range": "stddev: 0.15314068590227342",
            "extra": "mean: 817.0143964000018 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2465468362107173,
            "unit": "iter/sec",
            "range": "stddev: 0.14442401873088426",
            "extra": "mean: 802.2161469999986 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 292725.5071692917,
            "unit": "iter/sec",
            "range": "stddev: 6.236823062081429e-7",
            "extra": "mean: 3.416169672640351 usec\nrounds: 10479"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 285293.21610033355,
            "unit": "iter/sec",
            "range": "stddev: 6.602780523548793e-7",
            "extra": "mean: 3.5051657157116356 usec\nrounds: 60115"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 276310.3625282818,
            "unit": "iter/sec",
            "range": "stddev: 7.717737267917694e-7",
            "extra": "mean: 3.6191186998918465 usec\nrounds: 73530"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 135123.47304108617,
            "unit": "iter/sec",
            "range": "stddev: 9.056645655826535e-7",
            "extra": "mean: 7.40063867138714 usec\nrounds: 38054"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 157268.1065331192,
            "unit": "iter/sec",
            "range": "stddev: 9.504501622343707e-7",
            "extra": "mean: 6.35856832033143 usec\nrounds: 50051"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 304878.4542173116,
            "unit": "iter/sec",
            "range": "stddev: 5.737192047106919e-7",
            "extra": "mean: 3.2799956381542756 usec\nrounds: 74739"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 311093.8280167981,
            "unit": "iter/sec",
            "range": "stddev: 5.540033411186654e-7",
            "extra": "mean: 3.214464286787467 usec\nrounds: 67286"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 25863.915826585868,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023086607426064063",
            "extra": "mean: 38.66390560133537 usec\nrounds: 13104"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 376442.6063866309,
            "unit": "iter/sec",
            "range": "stddev: 5.362514610799649e-7",
            "extra": "mean: 2.656447445199482 usec\nrounds: 46989"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 170643.296808951,
            "unit": "iter/sec",
            "range": "stddev: 9.8001953787684e-7",
            "extra": "mean: 5.860177450272664 usec\nrounds: 50076"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 247807.32885678162,
            "unit": "iter/sec",
            "range": "stddev: 7.735419062027234e-7",
            "extra": "mean: 4.035393160538615 usec\nrounds: 50969"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 149859.9045188207,
            "unit": "iter/sec",
            "range": "stddev: 7.980150013268247e-7",
            "extra": "mean: 6.672898953264789 usec\nrounds: 43564"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 138060.6821155929,
            "unit": "iter/sec",
            "range": "stddev: 9.077213152459372e-7",
            "extra": "mean: 7.243191795639097 usec\nrounds: 28619"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 35432.479651208654,
            "unit": "iter/sec",
            "range": "stddev: 0.000001920394385199882",
            "extra": "mean: 28.222693129124213 usec\nrounds: 17698"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 17889.253943837914,
            "unit": "iter/sec",
            "range": "stddev: 0.00003819355452173815",
            "extra": "mean: 55.89948038858587 usec\nrounds: 11014"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 25540.01916342111,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024106052683081585",
            "extra": "mean: 39.154238436603 usec\nrounds: 8929"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 243.98351535178784,
            "unit": "iter/sec",
            "range": "stddev: 0.000039228027385055674",
            "extra": "mean: 4.098637559829192 msec\nrounds: 234"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 23.648181557116978,
            "unit": "iter/sec",
            "range": "stddev: 0.0011010014670477623",
            "extra": "mean: 42.2865494999994 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 21423.787990165507,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036950403096722894",
            "extra": "mean: 46.67708625846398 usec\nrounds: 12706"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 161.9908052067749,
            "unit": "iter/sec",
            "range": "stddev: 0.01493153713621084",
            "extra": "mean: 6.173189883978534 msec\nrounds: 181"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 10.834412038494705,
            "unit": "iter/sec",
            "range": "stddev: 0.08800586656351204",
            "extra": "mean: 92.29850188888851 msec\nrounds: 18"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 11405.744513219428,
            "unit": "iter/sec",
            "range": "stddev: 0.000004856123726960153",
            "extra": "mean: 87.67511834418043 usec\nrounds: 5653"
          }
        ]
      },
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
          "id": "751e0a7b5357519108e445faddda4fdc22a1a06c",
          "message": "release: v0.1.0 (merges PR #664)\n\nchore: update changelog for v0.1.0",
          "timestamp": "2026-04-21T03:18:27+01:00",
          "tree_id": "40f6ac7426657e4d1c8c05f8e73e52b58a4201f0",
          "url": "https://github.com/endavis/pynetappfoundry/commit/751e0a7b5357519108e445faddda4fdc22a1a06c"
        },
        "date": 1776737977127,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 841891.9659543559,
            "unit": "iter/sec",
            "range": "stddev: 3.1016183038484634e-7",
            "extra": "mean: 1.187800858589279 usec\nrounds: 44260"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 534566.8337464641,
            "unit": "iter/sec",
            "range": "stddev: 5.402247950868278e-7",
            "extra": "mean: 1.8706734815394155 usec\nrounds: 144488"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 363549.23055143026,
            "unit": "iter/sec",
            "range": "stddev: 6.57431689360252e-7",
            "extra": "mean: 2.7506591018861553 usec\nrounds: 120294"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 365698.54287248495,
            "unit": "iter/sec",
            "range": "stddev: 5.980851951445812e-7",
            "extra": "mean: 2.7344927112512147 usec\nrounds: 114903"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 370205.17137169675,
            "unit": "iter/sec",
            "range": "stddev: 5.841832619732645e-7",
            "extra": "mean: 2.7012048381030604 usec\nrounds: 62132"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 116403.47240590081,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010434524571507317",
            "extra": "mean: 8.590809013952638 usec\nrounds: 45019"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 106133.28682287996,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011466520830440367",
            "extra": "mean: 9.422114681785416 usec\nrounds: 57350"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 58698.98240201199,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015077944008827767",
            "extra": "mean: 17.03607045776868 usec\nrounds: 35610"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 177015.36655123727,
            "unit": "iter/sec",
            "range": "stddev: 8.119459397644967e-7",
            "extra": "mean: 5.649227067021603 usec\nrounds: 36901"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 23932.034578379364,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026534707030603",
            "extra": "mean: 41.784997289926125 usec\nrounds: 2583"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 67.20226124857237,
            "unit": "iter/sec",
            "range": "stddev: 0.0007565266766999135",
            "extra": "mean: 14.880451660713183 msec\nrounds: 56"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 64.6212175343497,
            "unit": "iter/sec",
            "range": "stddev: 0.0008523441527859997",
            "extra": "mean: 15.474793545455027 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 75.61048564653241,
            "unit": "iter/sec",
            "range": "stddev: 0.0006118138396397499",
            "extra": "mean: 13.225678838710929 msec\nrounds: 62"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 10.715407624422058,
            "unit": "iter/sec",
            "range": "stddev: 0.0003648244212213104",
            "extra": "mean: 93.32356127272719 msec\nrounds: 11"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 266.7478843142928,
            "unit": "iter/sec",
            "range": "stddev: 0.00006230667640457098",
            "extra": "mean: 3.7488582245764355 msec\nrounds: 236"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 65.47943155214706,
            "unit": "iter/sec",
            "range": "stddev: 0.0008796144108566725",
            "extra": "mean: 15.271971309091338 msec\nrounds: 55"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2089140107280996,
            "unit": "iter/sec",
            "range": "stddev: 0.14369727722272746",
            "extra": "mean: 827.1886926000008 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.196194279669064,
            "unit": "iter/sec",
            "range": "stddev: 0.15145756083861311",
            "extra": "mean: 835.9846029999886 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 287105.67986494716,
            "unit": "iter/sec",
            "range": "stddev: 6.984788116171897e-7",
            "extra": "mean: 3.4830380244319588 usec\nrounds: 8889"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 277360.05388219387,
            "unit": "iter/sec",
            "range": "stddev: 8.008222298535075e-7",
            "extra": "mean: 3.6054218551051367 usec\nrounds: 59684"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 273884.0856757051,
            "unit": "iter/sec",
            "range": "stddev: 9.466137320657796e-7",
            "extra": "mean: 3.6511796497152416 usec\nrounds: 62132"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 131221.5657749259,
            "unit": "iter/sec",
            "range": "stddev: 9.149412592772729e-7",
            "extra": "mean: 7.620698580256404 usec\nrounds: 35711"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 149124.67200207958,
            "unit": "iter/sec",
            "range": "stddev: 9.9627446797762e-7",
            "extra": "mean: 6.705798487765021 usec\nrounds: 50126"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 301856.7333840901,
            "unit": "iter/sec",
            "range": "stddev: 5.945799063311147e-7",
            "extra": "mean: 3.3128298606729265 usec\nrounds: 71271"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 305593.75470693246,
            "unit": "iter/sec",
            "range": "stddev: 6.080892930131353e-7",
            "extra": "mean: 3.272318182546009 usec\nrounds: 67191"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 25713.438381016804,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025366197816370633",
            "extra": "mean: 38.890170391924705 usec\nrounds: 11990"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 372939.7444940061,
            "unit": "iter/sec",
            "range": "stddev: 4.928942729442188e-7",
            "extra": "mean: 2.681398308342736 usec\nrounds: 45992"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 167322.02023514864,
            "unit": "iter/sec",
            "range": "stddev: 7.699420646156063e-7",
            "extra": "mean: 5.976499677655305 usec\nrounds: 49628"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 246956.69578519772,
            "unit": "iter/sec",
            "range": "stddev: 6.472924710936107e-7",
            "extra": "mean: 4.049292920851991 usec\nrounds: 52888"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 150815.09120337217,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010142251897587767",
            "extra": "mean: 6.6306361785208425 usec\nrounds: 44695"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 135706.22229764867,
            "unit": "iter/sec",
            "range": "stddev: 9.199640504469713e-7",
            "extra": "mean: 7.368858870794215 usec\nrounds: 52087"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 35352.35113208155,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023381638842969166",
            "extra": "mean: 28.286661791286633 usec\nrounds: 13264"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 17818.991352591634,
            "unit": "iter/sec",
            "range": "stddev: 0.000036398405141257015",
            "extra": "mean: 56.11989928119909 usec\nrounds: 11130"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 25222.440755885254,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026630718869045866",
            "extra": "mean: 39.64723357578572 usec\nrounds: 8798"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 244.1178310610849,
            "unit": "iter/sec",
            "range": "stddev: 0.00012788666060789628",
            "extra": "mean: 4.096382454544146 msec\nrounds: 231"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 23.307707299031055,
            "unit": "iter/sec",
            "range": "stddev: 0.0010670371080069218",
            "extra": "mean: 42.90426283333204 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 21602.90269915686,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026832645733863655",
            "extra": "mean: 46.29007564057717 usec\nrounds: 12176"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 160.94236481499806,
            "unit": "iter/sec",
            "range": "stddev: 0.01636708730265831",
            "extra": "mean: 6.213404414365925 msec\nrounds: 181"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 11.759798701465613,
            "unit": "iter/sec",
            "range": "stddev: 0.08382068267799489",
            "extra": "mean: 85.03546917647246 msec\nrounds: 17"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 11577.664610389085,
            "unit": "iter/sec",
            "range": "stddev: 0.000005330552443819676",
            "extra": "mean: 86.37320510240566 usec\nrounds: 4978"
          }
        ]
      },
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
          "id": "24c86cc8323a86b1cc37b401ada0413f0862dbc1",
          "message": "fix: split SBOMs into separate release artifact so twine accepts dist (merges PR #666, addresses #665)\n\nrelease.yml's build job generated SBOMs (sbom.json, sbom.xml) into\ndist/ alongside the wheels and sdist, then uploaded the whole directory\nas a single dist artifact. publish-testpypi and publish handed\npackages-dir: dist to pypa/gh-action-pypi-publish, which calls twine.\nTwine inspects every file in packages-dir and rejected sbom.json with\n\"InvalidDistribution: Unknown distribution format\". publish-testpypi\nfailed; publish and github-release were skipped (both needs: upstream).\n\nSplit the build output into two artifacts: dist (wheels + sdist only,\nconsumed by the publish jobs) and sbom (the SBOM files, consumed by\ngithub-release). github-release's download-artifact now grabs sbom into\ndist/ so the existing gh release upload line is unchanged. publish jobs\nare unchanged — they already only download the dist artifact and now\nget a twine-clean payload. New tests/test_release_workflow.py pins the\nartifact split via 3 structural YAML asserts. Synced\ndocs/development/release-and-automation.md SBOM bullet.\n\nPost-merge: re-run the failed release.yml run for v0.1.0 via Actions\n→ Release → Re-run failed jobs. skip-existing: true tolerates already-\nuploaded files and gh release upload --clobber handles re-upload.\n\nAddresses #665.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-21T03:50:45+01:00",
          "tree_id": "fffbf59bd88f5f943012f6c920c6778f1eff6b79",
          "url": "https://github.com/endavis/pynetappfoundry/commit/24c86cc8323a86b1cc37b401ada0413f0862dbc1"
        },
        "date": 1776739917178,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 841568.9213196117,
            "unit": "iter/sec",
            "range": "stddev: 3.627427374020869e-7",
            "extra": "mean: 1.188256807810776 usec\nrounds: 50824"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 535537.0851867399,
            "unit": "iter/sec",
            "range": "stddev: 5.021504775701053e-7",
            "extra": "mean: 1.8672843163630832 usec\nrounds: 155232"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 354556.9792319889,
            "unit": "iter/sec",
            "range": "stddev: 6.428031469764198e-7",
            "extra": "mean: 2.820421141239737 usec\nrounds: 81348"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 351210.72856617626,
            "unit": "iter/sec",
            "range": "stddev: 6.171106136402543e-7",
            "extra": "mean: 2.847293430022815 usec\nrounds: 127976"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 349743.81482709816,
            "unit": "iter/sec",
            "range": "stddev: 8.775752720422603e-7",
            "extra": "mean: 2.859235696546534 usec\nrounds: 67536"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 114841.89644678782,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012250986035551802",
            "extra": "mean: 8.707623532352164 usec\nrounds: 47781"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 104813.43982927524,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011572700784365134",
            "extra": "mean: 9.540761200365566 usec\nrounds: 54485"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 56103.122439317594,
            "unit": "iter/sec",
            "range": "stddev: 0.000001608790964043093",
            "extra": "mean: 17.824319868856186 usec\nrounds: 29584"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 176532.88801735197,
            "unit": "iter/sec",
            "range": "stddev: 0.000001275285509766766",
            "extra": "mean: 5.6646668574396575 usec\nrounds: 38434"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 23130.477588490296,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037797523817572578",
            "extra": "mean: 43.23300269846564 usec\nrounds: 2594"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 55.33349674797261,
            "unit": "iter/sec",
            "range": "stddev: 0.0010654008914436084",
            "extra": "mean: 18.072235784315207 msec\nrounds: 51"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 54.36849582403033,
            "unit": "iter/sec",
            "range": "stddev: 0.001136354200726852",
            "extra": "mean: 18.393004714285475 msec\nrounds: 49"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 63.378361324248196,
            "unit": "iter/sec",
            "range": "stddev: 0.0005369268740034047",
            "extra": "mean: 15.778255844828948 msec\nrounds: 58"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 9.652070800055139,
            "unit": "iter/sec",
            "range": "stddev: 0.0003718656464468145",
            "extra": "mean: 103.60471039999908 msec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 256.9392449470002,
            "unit": "iter/sec",
            "range": "stddev: 0.00009800833755193416",
            "extra": "mean: 3.8919706493504864 msec\nrounds: 231"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 51.45624286852462,
            "unit": "iter/sec",
            "range": "stddev: 0.002514589160426452",
            "extra": "mean: 19.433987875000724 msec\nrounds: 48"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.2889789576283694,
            "unit": "iter/sec",
            "range": "stddev: 0.12787894218979887",
            "extra": "mean: 775.8078547999958 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2779112127797374,
            "unit": "iter/sec",
            "range": "stddev: 0.12431073668326152",
            "extra": "mean: 782.5269783999943 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 284464.1893167545,
            "unit": "iter/sec",
            "range": "stddev: 7.940441012993372e-7",
            "extra": "mean: 3.515380977837204 usec\nrounds: 11208"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 276589.544696239,
            "unit": "iter/sec",
            "range": "stddev: 6.610087169824339e-7",
            "extra": "mean: 3.615465657236746 usec\nrounds: 67627"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 276289.83785756206,
            "unit": "iter/sec",
            "range": "stddev: 7.11029167938443e-7",
            "extra": "mean: 3.619387552413484 usec\nrounds: 75902"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 127819.39922543439,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011130836713131196",
            "extra": "mean: 7.823538571295469 usec\nrounds: 39252"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 148642.10824789706,
            "unit": "iter/sec",
            "range": "stddev: 9.88448574989297e-7",
            "extra": "mean: 6.727568733970426 usec\nrounds: 50259"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 299055.78476006066,
            "unit": "iter/sec",
            "range": "stddev: 7.048315445988154e-7",
            "extra": "mean: 3.3438577381217454 usec\nrounds: 73449"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 304575.72164465516,
            "unit": "iter/sec",
            "range": "stddev: 6.746854089473183e-7",
            "extra": "mean: 3.2832557848018102 usec\nrounds: 69363"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 23371.150029734352,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035000893094592336",
            "extra": "mean: 42.78779601036887 usec\nrounds: 12633"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 372190.0545479354,
            "unit": "iter/sec",
            "range": "stddev: 5.490828078994221e-7",
            "extra": "mean: 2.6867993590387766 usec\nrounds: 52726"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 168669.35012203336,
            "unit": "iter/sec",
            "range": "stddev: 9.488342505171882e-7",
            "extra": "mean: 5.928759429478406 usec\nrounds: 50692"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 245585.68755177472,
            "unit": "iter/sec",
            "range": "stddev: 7.547261520525461e-7",
            "extra": "mean: 4.07189852946613 usec\nrounds: 47738"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 147368.70059723582,
            "unit": "iter/sec",
            "range": "stddev: 9.562555902908562e-7",
            "extra": "mean: 6.785701413850675 usec\nrounds: 44560"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 135987.52108740425,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014035675333729891",
            "extra": "mean: 7.353615920075951 usec\nrounds: 53291"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 34164.51633441383,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025832154208566228",
            "extra": "mean: 29.270134844341484 usec\nrounds: 18221"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 16824.015648837532,
            "unit": "iter/sec",
            "range": "stddev: 0.00003119585287170643",
            "extra": "mean: 59.43884152705812 usec\nrounds: 10740"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 23864.456142158644,
            "unit": "iter/sec",
            "range": "stddev: 0.000003528683361578389",
            "extra": "mean: 41.90332241569138 usec\nrounds: 8793"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 230.1325921118658,
            "unit": "iter/sec",
            "range": "stddev: 0.000053725238965648035",
            "extra": "mean: 4.3453210639278215 msec\nrounds: 219"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 22.368901876528753,
            "unit": "iter/sec",
            "range": "stddev: 0.000614375223287943",
            "extra": "mean: 44.704921391303536 msec\nrounds: 23"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 19981.139279165523,
            "unit": "iter/sec",
            "range": "stddev: 0.000008920868262399903",
            "extra": "mean: 50.04719630990748 usec\nrounds: 12791"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 153.33341798082074,
            "unit": "iter/sec",
            "range": "stddev: 0.015895209242166967",
            "extra": "mean: 6.521735530118308 msec\nrounds: 166"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 11.049683946841013,
            "unit": "iter/sec",
            "range": "stddev: 0.08022161555631442",
            "extra": "mean: 90.50032605556011 msec\nrounds: 18"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 9990.541724277657,
            "unit": "iter/sec",
            "range": "stddev: 0.000007914071110201087",
            "extra": "mean: 100.09467230089595 usec\nrounds: 5798"
          }
        ]
      },
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
          "id": "6aee3f627ac1c175554e573df460c6bfaf79d5de",
          "message": "fix: bump lxml to 6.1.0 in uv.lock to resolve CVE-2026-41066 (merges PR #670, addresses #669)\n\npip-audit flags lxml 6.0.2 for CVE-2026-41066 with a fix in 6.1.0.\nlxml is a transitive dependency via cyclonedx-python-lib, pulled in\nthrough both cyclonedx-bom[validation] and pip-audit under the\nsecurity extra. Since pip-audit --skip-editable inspects the\nresolved lockfile, the CVE blocks CI on every branch until the lock\nis regenerated.\n\nRegenerated via: uv lock --upgrade-package lxml\n\nNo pyproject.toml change — the bump is lock-only, matching the\nupstream pyproject-template fix (#460).\n\nAddresses #669.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-23T18:45:25+01:00",
          "tree_id": "612923f9d6b0ecef2bd8a0e90cbf1e0b391e6daf",
          "url": "https://github.com/endavis/pynetappfoundry/commit/6aee3f627ac1c175554e573df460c6bfaf79d5de"
        },
        "date": 1776966408592,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 823852.1660369227,
            "unit": "iter/sec",
            "range": "stddev: 3.437252941903449e-7",
            "extra": "mean: 1.2138100028436205 usec\nrounds: 49906"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 536707.1817547256,
            "unit": "iter/sec",
            "range": "stddev: 4.961433165682658e-7",
            "extra": "mean: 1.8632133759242269 usec\nrounds: 161499"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 352305.17455518834,
            "unit": "iter/sec",
            "range": "stddev: 6.989862557230774e-7",
            "extra": "mean: 2.8384482324523757 usec\nrounds: 130294"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 351454.0643267123,
            "unit": "iter/sec",
            "range": "stddev: 6.08221000718657e-7",
            "extra": "mean: 2.8453220534402424 usec\nrounds: 131857"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 363492.5842975752,
            "unit": "iter/sec",
            "range": "stddev: 6.291919582737168e-7",
            "extra": "mean: 2.751087761343006 usec\nrounds: 27928"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 115399.87849212805,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012165368631909012",
            "extra": "mean: 8.665520389332253 usec\nrounds: 49315"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 104964.54007776809,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010866476303876845",
            "extra": "mean: 9.52702692984794 usec\nrounds: 53955"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 55971.30005638263,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019116449214058574",
            "extra": "mean: 17.86629931755473 usec\nrounds: 36777"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 175496.82594335964,
            "unit": "iter/sec",
            "range": "stddev: 9.46283132895066e-7",
            "extra": "mean: 5.698108752820082 usec\nrounds: 40330"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 23442.343874260376,
            "unit": "iter/sec",
            "range": "stddev: 0.000004200195648451418",
            "extra": "mean: 42.65785048473745 usec\nrounds: 2682"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 58.05840603128424,
            "unit": "iter/sec",
            "range": "stddev: 0.0012662934192737426",
            "extra": "mean: 17.224034698113467 msec\nrounds: 53"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 59.08609571732535,
            "unit": "iter/sec",
            "range": "stddev: 0.001014930991438993",
            "extra": "mean: 16.92445553999903 msec\nrounds: 50"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 64.66495716948596,
            "unit": "iter/sec",
            "range": "stddev: 0.0013979365600419393",
            "extra": "mean: 15.464326333334046 msec\nrounds: 54"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 9.477917672105798,
            "unit": "iter/sec",
            "range": "stddev: 0.0007952341844976062",
            "extra": "mean: 105.50840750000106 msec\nrounds: 10"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 256.4933676183724,
            "unit": "iter/sec",
            "range": "stddev: 0.000025952023608268967",
            "extra": "mean: 3.8987362881361727 msec\nrounds: 236"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 55.83166332513265,
            "unit": "iter/sec",
            "range": "stddev: 0.001998873789810574",
            "extra": "mean: 17.910983489360767 msec\nrounds: 47"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.3038451493377792,
            "unit": "iter/sec",
            "range": "stddev: 0.12273113810459947",
            "extra": "mean: 766.9622427999968 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.2967024140792862,
            "unit": "iter/sec",
            "range": "stddev: 0.12295972519648177",
            "extra": "mean: 771.1869656000005 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 286621.7122617913,
            "unit": "iter/sec",
            "range": "stddev: 7.336186192235906e-7",
            "extra": "mean: 3.488919217280481 usec\nrounds: 9148"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 280528.61841420544,
            "unit": "iter/sec",
            "range": "stddev: 8.582891330229272e-7",
            "extra": "mean: 3.56469869510241 usec\nrounds: 67669"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 277513.8342009786,
            "unit": "iter/sec",
            "range": "stddev: 6.940806481658127e-7",
            "extra": "mean: 3.603423962193499 usec\nrounds: 79158"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 131494.97022959046,
            "unit": "iter/sec",
            "range": "stddev: 0.000001047349343403469",
            "extra": "mean: 7.604853617244813 usec\nrounds: 39547"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 151371.15103304636,
            "unit": "iter/sec",
            "range": "stddev: 0.000001044220494213719",
            "extra": "mean: 6.606278628228747 usec\nrounds: 48929"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 302894.603270785,
            "unit": "iter/sec",
            "range": "stddev: 6.151829217598028e-7",
            "extra": "mean: 3.301478432436808 usec\nrounds: 76782"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 306485.8590772765,
            "unit": "iter/sec",
            "range": "stddev: 6.255052735022241e-7",
            "extra": "mean: 3.2627932753917457 usec\nrounds: 72807"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 23966.680971147085,
            "unit": "iter/sec",
            "range": "stddev: 0.000003235794658736778",
            "extra": "mean: 41.724592621059045 usec\nrounds: 12983"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 343646.9245884981,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010914033357734935",
            "extra": "mean: 2.9099634783505066 usec\nrounds: 53749"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 172322.06139556284,
            "unit": "iter/sec",
            "range": "stddev: 8.554591416558738e-7",
            "extra": "mean: 5.803087497337409 usec\nrounds: 51293"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 243221.16496721853,
            "unit": "iter/sec",
            "range": "stddev: 9.807306076385122e-7",
            "extra": "mean: 4.11148429510557 usec\nrounds: 57498"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 148303.72565684674,
            "unit": "iter/sec",
            "range": "stddev: 9.213341120995391e-7",
            "extra": "mean: 6.742918935926496 usec\nrounds: 44582"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 137065.3053118019,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012366904320182315",
            "extra": "mean: 7.295792306631924 usec\nrounds: 57166"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 34257.66983028462,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022951572080036196",
            "extra": "mean: 29.19054345943797 usec\nrounds: 18546"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 16308.783339906708,
            "unit": "iter/sec",
            "range": "stddev: 0.0000382466583398318",
            "extra": "mean: 61.31665245396046 usec\nrounds: 8537"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 24217.339242120164,
            "unit": "iter/sec",
            "range": "stddev: 0.000003504111346616863",
            "extra": "mean: 41.292727908801126 usec\nrounds: 9291"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 233.09460449429622,
            "unit": "iter/sec",
            "range": "stddev: 0.00019740169095618413",
            "extra": "mean: 4.290103591927928 msec\nrounds: 223"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 22.602323265095094,
            "unit": "iter/sec",
            "range": "stddev: 0.0008099741394254131",
            "extra": "mean: 44.243239434784385 msec\nrounds: 23"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 20427.388120910084,
            "unit": "iter/sec",
            "range": "stddev: 0.0000045200398529727895",
            "extra": "mean: 48.953884563262896 usec\nrounds: 12535"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 158.41831889407584,
            "unit": "iter/sec",
            "range": "stddev: 0.013958114577061233",
            "extra": "mean: 6.312401286549669 msec\nrounds: 171"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 11.244034863816301,
            "unit": "iter/sec",
            "range": "stddev: 0.07691511291461403",
            "extra": "mean: 88.9360458333365 msec\nrounds: 18"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 10132.638885130264,
            "unit": "iter/sec",
            "range": "stddev: 0.000006807019174940315",
            "extra": "mean: 98.69097392462183 usec\nrounds: 6021"
          }
        ]
      },
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
          "id": "36c322f3902781b45079298f2d0e7faa69e90fe1",
          "message": "chore: sync with pyproject-template (64c7aca0 → 0cdab3e) (merges PR #668, addresses #667)\n\n* chore: sync with pyproject-template (64c7aca0 → 0cdab3e)\n\nSyncs to upstream pyproject-template commit 0cdab3e (2026-04-22),\ncovering ~30 upstream commits touching 136 files. Key changes:\n\nTooling (tools/doit/, tools/pyproject_template/, tools/hooks/ai/):\nUTF-8 encoding hardening, new PyPI environment helper tasks,\nplaceholder marker tokens (upstream #464/#468), refreshed hooks.\n\nWorkflows (.github/): refreshed 7 workflows (dedupe, App-token\nready-to-merge, concurrency, codecov gating, python-versions\nextraction). Added composite action python-versions/action.yml,\nnew workflows ci-full-matrix.yml and dependabot-blocked-label.yml.\n\nPre-commit: added actionlint hook (upstream #415/#416).\n\nDocs: refreshed 11 template-owned development docs, updated ADR\nREADME as a two-series index (9XXX template-meta + 0001+ project),\nregenerated TABLE_OF_CONTENTS.md.\n\nADRs: added 16 template-meta ADRs (9001-9016) documenting\ninherited tooling decisions (uv, doit, ruff, mypy, pytest, mkdocs,\nconventional commits, merge gate, etc.). Project ADRs 0001-0016\nleft untouched.\n\nContributor instructions: renamed issue type doc → docs across\nAGENTS.md, .github/CONTRIBUTING.md, tools/doit/github.py,\ntools/doit/templates.py. Unblocks docs-typed PRs that were\nfailing the Validate PR Title Format check. Cache-schema\npitfalls and other project-specific content preserved.\n\nDependencies: bumped mkdocstrings[python] >=1.0.4, regenerated\nuv.lock. Ruff/pyproject-fmt/hypothesis bumps deferred to open\ndependabot PRs #623-#629.\n\nSettings pointer (.config/pyproject_template/settings.toml):\nbumped to 0cdab3e349b2bfd8007acb713b136b134bf0700e, 2026-04-22.\n\nDeleted tests/test_doit_github.py and tests/test_doit_release.py\nper upstream #463 strip-on-spawn behavior. bootstrap.py addition\nskipped per project memory.\n\nAddresses #667.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n* fix: restore SOPS install tasks stripped by template sync\n\nThe template sync replaced tools/doit/install_tools.py with the\nupstream framework-only version, stripping this project's SOPS-\nspecific task_install_age / task_install_sops / task_install_tools\ndefinitions. CI on ubuntu-latest and windows-latest failed at the\n\"Install SOPS tools\" step with:\n\n  ERROR: Invalid parameter: \"install_tools\". Must be a command,\n  task, or a target.\n\nRestoring the tasks in a dedicated tools/doit/install_sops.py\nso future template refreshes do not overwrite them. The module\nimports create_install_task / get_install_dir /\nget_latest_github_release from the template-owned install_tools\nframework.\n\ndoit auto-discovery picks up the three tasks from any tools/doit/\nfile, so ci.yml's `uv run doit install_tools` invocation works\nunchanged.\n\nAddresses #667.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n* docs: reference upstream issue #477 in install_sops.py\n\nPoints future readers to\nhttps://github.com/endavis/pyproject-template/issues/477, which\ntracks adding per-platform extract_binaries support to the\ninstall_tool framework. Once that lands, _install_age can collapse\nto a single create_install_task call.\n\nAddresses #667.\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>\n\n---------\n\nCo-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
          "timestamp": "2026-04-23T19:22:04+01:00",
          "tree_id": "f2fe32dcc67102c487c80ee1a1bea9535deaa1e6",
          "url": "https://github.com/endavis/pynetappfoundry/commit/36c322f3902781b45079298f2d0e7faa69e90fe1"
        },
        "date": 1776968595602,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1114591.8362235911,
            "unit": "iter/sec",
            "range": "stddev: 3.2343366681490725e-7",
            "extra": "mean: 897.1894172382907 nsec\nrounds: 67903"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 724768.8415213726,
            "unit": "iter/sec",
            "range": "stddev: 4.6519215865379153e-7",
            "extra": "mean: 1.3797502634093457 usec\nrounds: 194553"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 425352.6965662378,
            "unit": "iter/sec",
            "range": "stddev: 6.333774387245801e-7",
            "extra": "mean: 2.350990150227661 usec\nrounds: 147211"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 442375.3184025443,
            "unit": "iter/sec",
            "range": "stddev: 5.734568316697132e-7",
            "extra": "mean: 2.26052394516739 usec\nrounds: 167758"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 499915.7975244451,
            "unit": "iter/sec",
            "range": "stddev: 5.406525699177118e-7",
            "extra": "mean: 2.000336866632228 usec\nrounds: 82359"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 157798.38024328038,
            "unit": "iter/sec",
            "range": "stddev: 9.42876690585413e-7",
            "extra": "mean: 6.337200663646126 usec\nrounds: 56358"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 138288.21727657955,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010635156837200027",
            "extra": "mean: 7.231274071600601 usec\nrounds: 70737"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 69553.01846875196,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014015653302360015",
            "extra": "mean: 14.377521235103108 usec\nrounds: 45891"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 231465.98012260924,
            "unit": "iter/sec",
            "range": "stddev: 9.80117418265649e-7",
            "extra": "mean: 4.320289311933843 usec\nrounds: 47015"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31480.457661588414,
            "unit": "iter/sec",
            "range": "stddev: 0.000002574757364999802",
            "extra": "mean: 31.76573894667905 usec\nrounds: 3076"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 83.52990524734024,
            "unit": "iter/sec",
            "range": "stddev: 0.0008146675963981116",
            "extra": "mean: 11.971760258064487 msec\nrounds: 62"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 81.01544622572817,
            "unit": "iter/sec",
            "range": "stddev: 0.00103738128664532",
            "extra": "mean: 12.343325212500389 msec\nrounds: 80"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 91.48575344691861,
            "unit": "iter/sec",
            "range": "stddev: 0.00073828346471133",
            "extra": "mean: 10.93066365333281 msec\nrounds: 75"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 12.250585026923346,
            "unit": "iter/sec",
            "range": "stddev: 0.0009634832961499388",
            "extra": "mean: 81.62875469230904 msec\nrounds: 13"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 335.1694675425698,
            "unit": "iter/sec",
            "range": "stddev: 0.00008602163088227",
            "extra": "mean: 2.9835653209461572 msec\nrounds: 296"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 84.24270247083133,
            "unit": "iter/sec",
            "range": "stddev: 0.0007200700996885576",
            "extra": "mean: 11.870464392405331 msec\nrounds: 79"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 1.4064411589113832,
            "unit": "iter/sec",
            "range": "stddev: 0.1475826054451738",
            "extra": "mean: 711.0144592000012 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 1.352289440383876,
            "unit": "iter/sec",
            "range": "stddev: 0.14926057162816025",
            "extra": "mean: 739.4866588000042 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 411680.5147804233,
            "unit": "iter/sec",
            "range": "stddev: 7.154050848239209e-7",
            "extra": "mean: 2.4290680858028137 usec\nrounds: 11603"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 384312.7455138633,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013196183980095908",
            "extra": "mean: 2.60204745138729 usec\nrounds: 80103"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 388098.2969995254,
            "unit": "iter/sec",
            "range": "stddev: 7.538518319075378e-7",
            "extra": "mean: 2.576666807690792 usec\nrounds: 89840"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 172223.66927127694,
            "unit": "iter/sec",
            "range": "stddev: 8.830723715113946e-7",
            "extra": "mean: 5.806402826227426 usec\nrounds: 44441"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 202065.78686324478,
            "unit": "iter/sec",
            "range": "stddev: 8.019072201539487e-7",
            "extra": "mean: 4.948883309358974 usec\nrounds: 61196"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 436728.6945938012,
            "unit": "iter/sec",
            "range": "stddev: 6.055703428412255e-7",
            "extra": "mean: 2.2897510797409226 usec\nrounds: 102575"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 445035.57377182564,
            "unit": "iter/sec",
            "range": "stddev: 5.466991334937037e-7",
            "extra": "mean: 2.2470113827635503 usec\nrounds: 77310"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 34413.025256509296,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024022709859002206",
            "extra": "mean: 29.058764597013973 usec\nrounds: 17281"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 566910.7578666434,
            "unit": "iter/sec",
            "range": "stddev: 4.7268980224670904e-7",
            "extra": "mean: 1.7639460640385907 usec\nrounds: 57661"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 262319.7847038481,
            "unit": "iter/sec",
            "range": "stddev: 7.195246304141898e-7",
            "extra": "mean: 3.812140975675825 usec\nrounds: 84660"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 371457.48432655085,
            "unit": "iter/sec",
            "range": "stddev: 6.022297206990052e-7",
            "extra": "mean: 2.6920981328805134 usec\nrounds: 77018"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 226300.9514449565,
            "unit": "iter/sec",
            "range": "stddev: 7.663933284046113e-7",
            "extra": "mean: 4.418894368825628 usec\nrounds: 60787"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 210550.67854735767,
            "unit": "iter/sec",
            "range": "stddev: 8.223756840563299e-7",
            "extra": "mean: 4.749450378879103 usec\nrounds: 82082"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 52264.26661309554,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020141216002698786",
            "extra": "mean: 19.13353166137102 usec\nrounds: 25678"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26221.331099373325,
            "unit": "iter/sec",
            "range": "stddev: 0.00004448843497217277",
            "extra": "mean: 38.136889245256484 usec\nrounds: 14031"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35773.47449072354,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027190181974519026",
            "extra": "mean: 27.953672776719273 usec\nrounds: 11020"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 334.69319742547276,
            "unit": "iter/sec",
            "range": "stddev: 0.00017875218556010364",
            "extra": "mean: 2.987810949526912 msec\nrounds: 317"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 34.06664508878836,
            "unit": "iter/sec",
            "range": "stddev: 0.0004106522670622652",
            "extra": "mean: 29.35422602941048 msec\nrounds: 34"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 29176.422184446186,
            "unit": "iter/sec",
            "range": "stddev: 0.000003323627567179073",
            "extra": "mean: 34.2742504093972 usec\nrounds: 16485"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 225.67527434204948,
            "unit": "iter/sec",
            "range": "stddev: 0.011602992345633419",
            "extra": "mean: 4.431145604743251 msec\nrounds: 253"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 15.516154469345542,
            "unit": "iter/sec",
            "range": "stddev: 0.0698885681600611",
            "extra": "mean: 64.44895879166761 msec\nrounds: 24"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 15345.138180363034,
            "unit": "iter/sec",
            "range": "stddev: 0.0000073406987652837285",
            "extra": "mean: 65.16722027825638 usec\nrounds: 7259"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "49699333+dependabot[bot]@users.noreply.github.com",
            "name": "dependabot[bot]",
            "username": "dependabot[bot]"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "bff2eb8110f5b9083c430d9d021157e9cf4df5db",
          "message": "chore(deps): Bump cryptography from 46.0.7 to 47.0.0 (merges PR #674)\n\nBumps [cryptography](https://github.com/pyca/cryptography) from 46.0.7 to 47.0.0.\n- [Changelog](https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst)\n- [Commits](https://github.com/pyca/cryptography/compare/46.0.7...47.0.0)\n\n---\nupdated-dependencies:\n- dependency-name: cryptography\n  dependency-version: 47.0.0\n  dependency-type: direct:production\n  update-type: version-update:semver-major\n...\n\nSigned-off-by: dependabot[bot] <support@github.com>\nCo-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>",
          "timestamp": "2026-04-28T14:06:53+01:00",
          "tree_id": "146dc55dd46d30b9f262350cdf5e74475124c6ea",
          "url": "https://github.com/endavis/pynetappfoundry/commit/bff2eb8110f5b9083c430d9d021157e9cf4df5db"
        },
        "date": 1777381946252,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1108063.5487523025,
            "unit": "iter/sec",
            "range": "stddev: 3.7220719775053527e-7",
            "extra": "mean: 902.4753148192775 nsec\nrounds: 50739"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 504077.6184437156,
            "unit": "iter/sec",
            "range": "stddev: 9.547309599740518e-7",
            "extra": "mean: 1.9838214660023794 usec\nrounds: 53396"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 466370.2641148955,
            "unit": "iter/sec",
            "range": "stddev: 5.982133793838892e-7",
            "extra": "mean: 2.1442190399893057 usec\nrounds: 134391"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 466797.09941113763,
            "unit": "iter/sec",
            "range": "stddev: 5.485453175668039e-7",
            "extra": "mean: 2.1422583843419236 usec\nrounds: 101678"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 519331.71583444317,
            "unit": "iter/sec",
            "range": "stddev: 5.352346935045441e-7",
            "extra": "mean: 1.9255515685061457 usec\nrounds: 71119"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 159100.69213103564,
            "unit": "iter/sec",
            "range": "stddev: 9.101506155616431e-7",
            "extra": "mean: 6.285327779569922 usec\nrounds: 27009"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 141320.70666073475,
            "unit": "iter/sec",
            "range": "stddev: 9.156897021130293e-7",
            "extra": "mean: 7.076103874860151 usec\nrounds: 67331"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 75397.78107043184,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013157757624192118",
            "extra": "mean: 13.262989783026415 usec\nrounds: 41989"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 225441.4995949901,
            "unit": "iter/sec",
            "range": "stddev: 7.553186851892928e-7",
            "extra": "mean: 4.435740543761991 usec\nrounds: 40053"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 32937.66393105198,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018087855955561765",
            "extra": "mean: 30.360380204658348 usec\nrounds: 2738"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 47.684241835703126,
            "unit": "iter/sec",
            "range": "stddev: 0.0026175291783970206",
            "extra": "mean: 20.971288658536654 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 45.296870445785856,
            "unit": "iter/sec",
            "range": "stddev: 0.001982330407578445",
            "extra": "mean: 22.076580350001507 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 53.181556651623424,
            "unit": "iter/sec",
            "range": "stddev: 0.0024783486766806295",
            "extra": "mean: 18.803511272727555 msec\nrounds: 44"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.435687054860937,
            "unit": "iter/sec",
            "range": "stddev: 0.000827958260147074",
            "extra": "mean: 118.54398977778165 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 306.69595107854866,
            "unit": "iter/sec",
            "range": "stddev: 0.00006404358108314731",
            "extra": "mean: 3.2605582058821754 msec\nrounds: 170"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 56.90617679317815,
            "unit": "iter/sec",
            "range": "stddev: 0.0011393744635381283",
            "extra": "mean: 17.572784825001264 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.0734550989705129,
            "unit": "iter/sec",
            "range": "stddev: 0.2105418393778912",
            "extra": "mean: 13.613758799800001 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.07543284196517562,
            "unit": "iter/sec",
            "range": "stddev: 0.10213461573200995",
            "extra": "mean: 13.256825196400007 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 417754.06773222267,
            "unit": "iter/sec",
            "range": "stddev: 4.940117162098951e-7",
            "extra": "mean: 2.393752873379542 usec\nrounds: 12095"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 392802.35045045946,
            "unit": "iter/sec",
            "range": "stddev: 5.161132039249954e-7",
            "extra": "mean: 2.5458096135453774 usec\nrounds: 65262"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 391836.4190787085,
            "unit": "iter/sec",
            "range": "stddev: 4.773971549057838e-7",
            "extra": "mean: 2.5520853889774067 usec\nrounds: 83348"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 177214.87369237436,
            "unit": "iter/sec",
            "range": "stddev: 7.85953700991543e-7",
            "extra": "mean: 5.642867210660268 usec\nrounds: 43264"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 208113.75410305746,
            "unit": "iter/sec",
            "range": "stddev: 6.611166209484225e-7",
            "extra": "mean: 4.805064443289041 usec\nrounds: 60332"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 437305.10711936926,
            "unit": "iter/sec",
            "range": "stddev: 4.661341079581056e-7",
            "extra": "mean: 2.2867329553666393 usec\nrounds: 80979"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 447426.6145713148,
            "unit": "iter/sec",
            "range": "stddev: 4.6660362847353535e-7",
            "extra": "mean: 2.2350033892331433 usec\nrounds: 90286"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35862.61633314373,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021005451871695956",
            "extra": "mean: 27.88418978444174 usec\nrounds: 15486"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 576017.509263623,
            "unit": "iter/sec",
            "range": "stddev: 4.458865996606629e-7",
            "extra": "mean: 1.7360583383626538 usec\nrounds: 57955"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 262296.60914308764,
            "unit": "iter/sec",
            "range": "stddev: 6.423760209822741e-7",
            "extra": "mean: 3.812477802389285 usec\nrounds: 61448"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 373977.1115666101,
            "unit": "iter/sec",
            "range": "stddev: 4.847750143133769e-7",
            "extra": "mean: 2.673960435201359 usec\nrounds: 56161"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 230065.7894702361,
            "unit": "iter/sec",
            "range": "stddev: 7.114955299629279e-7",
            "extra": "mean: 4.346582785309639 usec\nrounds: 40907"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 209385.00793155876,
            "unit": "iter/sec",
            "range": "stddev: 6.76105021062721e-7",
            "extra": "mean: 4.775891119801986 usec\nrounds: 71069"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 54165.64938582753,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014152844943392078",
            "extra": "mean: 18.461885186253312 usec\nrounds: 19867"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26988.23984216652,
            "unit": "iter/sec",
            "range": "stddev: 0.0000725531599167939",
            "extra": "mean: 37.05317597028304 usec\nrounds: 13991"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 36207.16807853084,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018910977850707564",
            "extra": "mean: 27.61884049675107 usec\nrounds: 9097"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 338.33925025977925,
            "unit": "iter/sec",
            "range": "stddev: 0.00007898847583200307",
            "extra": "mean: 2.955613335526969 msec\nrounds: 304"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 31.224513022716827,
            "unit": "iter/sec",
            "range": "stddev: 0.0008052306841520986",
            "extra": "mean: 32.02611996774676 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 975.2216147609238,
            "unit": "iter/sec",
            "range": "stddev: 0.0010830601361856013",
            "extra": "mean: 1.0254079532939295 msec\nrounds: 1199"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 7.878275055073164,
            "unit": "iter/sec",
            "range": "stddev: 0.0027426309136602766",
            "extra": "mean: 126.93133877777679 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.7851762198290769,
            "unit": "iter/sec",
            "range": "stddev: 0.1179975731156025",
            "extra": "mean: 1.2735994477999952 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 946.6241375730007,
            "unit": "iter/sec",
            "range": "stddev: 0.001048562738760636",
            "extra": "mean: 1.056385486391512 msec\nrounds: 1139"
          }
        ]
      },
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
          "id": "d4973b8bb9a495f878a630a74469fb0d11069d50",
          "message": "feat: validate where expressions before query execution (merges PR #682, addresses #618)\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-05-05T16:11:51+01:00",
          "tree_id": "b5b07591f2304bd6b5fc203c9d3cc242849b487f",
          "url": "https://github.com/endavis/pynetappfoundry/commit/d4973b8bb9a495f878a630a74469fb0d11069d50"
        },
        "date": 1777994255428,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1202998.2036865363,
            "unit": "iter/sec",
            "range": "stddev: 2.7730671571658504e-7",
            "extra": "mean: 831.2564365728418 nsec\nrounds: 50687"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 746318.985233784,
            "unit": "iter/sec",
            "range": "stddev: 5.046956233231054e-7",
            "extra": "mean: 1.3399096362083711 usec\nrounds: 181555"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 477469.494725125,
            "unit": "iter/sec",
            "range": "stddev: 5.227229670045067e-7",
            "extra": "mean: 2.094374637641911 usec\nrounds: 164204"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 475718.02697111364,
            "unit": "iter/sec",
            "range": "stddev: 5.572017057693868e-7",
            "extra": "mean: 2.1020855702420578 usec\nrounds: 126551"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 516656.28993886494,
            "unit": "iter/sec",
            "range": "stddev: 4.818850099867774e-7",
            "extra": "mean: 1.93552274398581 usec\nrounds: 72041"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 164887.92958429342,
            "unit": "iter/sec",
            "range": "stddev: 9.278346858528746e-7",
            "extra": "mean: 6.064725310828671 usec\nrounds: 54771"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 144018.57640468894,
            "unit": "iter/sec",
            "range": "stddev: 9.929097651673741e-7",
            "extra": "mean: 6.9435487071474915 usec\nrounds: 67331"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 78637.40846018643,
            "unit": "iter/sec",
            "range": "stddev: 0.000001672967050158036",
            "extra": "mean: 12.716594043231892 usec\nrounds: 44655"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 240606.7814615903,
            "unit": "iter/sec",
            "range": "stddev: 7.038029647820741e-7",
            "extra": "mean: 4.156158832786834 usec\nrounds: 40508"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 32537.074585716535,
            "unit": "iter/sec",
            "range": "stddev: 0.000002211431768566947",
            "extra": "mean: 30.73417056489124 usec\nrounds: 2779"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 49.4647957388137,
            "unit": "iter/sec",
            "range": "stddev: 0.0017954381557863028",
            "extra": "mean: 20.216398047618476 msec\nrounds: 42"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 50.139816345389676,
            "unit": "iter/sec",
            "range": "stddev: 0.002045770956067758",
            "extra": "mean: 19.944229414632655 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 77.51914091252306,
            "unit": "iter/sec",
            "range": "stddev: 0.001059606947593027",
            "extra": "mean: 12.90003976086959 msec\nrounds: 46"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.476155406074792,
            "unit": "iter/sec",
            "range": "stddev: 0.0012603836798925285",
            "extra": "mean: 117.97801622222595 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 292.6748451691527,
            "unit": "iter/sec",
            "range": "stddev: 0.0003122423310049274",
            "extra": "mean: 3.4167610114290676 msec\nrounds: 175"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 65.6619120586047,
            "unit": "iter/sec",
            "range": "stddev: 0.0016653155215679422",
            "extra": "mean: 15.229529093022421 msec\nrounds: 43"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.07129310122988654,
            "unit": "iter/sec",
            "range": "stddev: 0.3141994168668526",
            "extra": "mean: 14.026602613 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.07451103357464275,
            "unit": "iter/sec",
            "range": "stddev: 0.21102986510983532",
            "extra": "mean: 13.420831144400006 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 403568.4865248838,
            "unit": "iter/sec",
            "range": "stddev: 5.291976046025706e-7",
            "extra": "mean: 2.477894170109689 usec\nrounds: 11509"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 385514.0209528876,
            "unit": "iter/sec",
            "range": "stddev: 5.559936489969856e-7",
            "extra": "mean: 2.593939378724196 usec\nrounds: 48168"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 383163.39053135476,
            "unit": "iter/sec",
            "range": "stddev: 5.761517339537722e-7",
            "extra": "mean: 2.609852675677711 usec\nrounds: 62135"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 173558.00714940345,
            "unit": "iter/sec",
            "range": "stddev: 7.306952175943111e-7",
            "extra": "mean: 5.761762401081113 usec\nrounds: 36469"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 205825.6751761196,
            "unit": "iter/sec",
            "range": "stddev: 7.313915181402075e-7",
            "extra": "mean: 4.858480357925834 usec\nrounds: 41467"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 416288.01472937345,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014263006360462266",
            "extra": "mean: 2.4021830190093136 usec\nrounds: 60043"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 430681.2542428668,
            "unit": "iter/sec",
            "range": "stddev: 4.784727366023498e-7",
            "extra": "mean: 2.3219027764697806 usec\nrounds: 67422"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35751.272508788585,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020955699810624612",
            "extra": "mean: 27.971032352881263 usec\nrounds: 14682"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 597269.0887843375,
            "unit": "iter/sec",
            "range": "stddev: 4.0133321304438433e-7",
            "extra": "mean: 1.6742872162283973 usec\nrounds: 55164"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 263193.45560504467,
            "unit": "iter/sec",
            "range": "stddev: 6.345257833507348e-7",
            "extra": "mean: 3.799486570443558 usec\nrounds: 55289"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 361946.0420942333,
            "unit": "iter/sec",
            "range": "stddev: 5.37719783306956e-7",
            "extra": "mean: 2.7628427547210155 usec\nrounds: 51709"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 230255.0768550125,
            "unit": "iter/sec",
            "range": "stddev: 7.606436806745052e-7",
            "extra": "mean: 4.3430095599137735 usec\nrounds: 46549"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 205144.5352020511,
            "unit": "iter/sec",
            "range": "stddev: 6.639335656903312e-7",
            "extra": "mean: 4.874611936482146 usec\nrounds: 62799"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 53025.19641697545,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015078566941858558",
            "extra": "mean: 18.85895890203361 usec\nrounds: 20512"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26481.510127608988,
            "unit": "iter/sec",
            "range": "stddev: 0.00006691390227285229",
            "extra": "mean: 37.76219691328796 usec\nrounds: 13087"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 36670.09463807649,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018366775682183014",
            "extra": "mean: 27.270177780278956 usec\nrounds: 9028"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 341.9105656053709,
            "unit": "iter/sec",
            "range": "stddev: 0.00003403824948616155",
            "extra": "mean: 2.924741440000389 msec\nrounds: 300"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 30.88015148155104,
            "unit": "iter/sec",
            "range": "stddev: 0.0007481547016643131",
            "extra": "mean: 32.38326083333618 msec\nrounds: 30"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 968.6992601845539,
            "unit": "iter/sec",
            "range": "stddev: 0.0011052627695848703",
            "extra": "mean: 1.0323121334989798 msec\nrounds: 1206"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 7.671075571325032,
            "unit": "iter/sec",
            "range": "stddev: 0.0027379881003430423",
            "extra": "mean: 130.3598159999966 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.7596701057874777,
            "unit": "iter/sec",
            "range": "stddev: 0.13222325827668327",
            "extra": "mean: 1.3163608682000132 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 917.0913722670729,
            "unit": "iter/sec",
            "range": "stddev: 0.0011033892920540233",
            "extra": "mean: 1.0904038902121334 msec\nrounds: 1175"
          }
        ]
      },
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
          "id": "e7a91ed1fd62add94ade0ee3e39afe8287b60f93",
          "message": "fix: QueryBuilder.filter() leaves partial state on early-validation rejection (merges PR #684, addresses #683)\n\nfix: address review feedback for early where validation\n\n- Hoist filter() validation above state mutation so a rejected call\n  leaves the QueryBuilder in its prior state instead of with partially\n  applied equality filters.\n- Switch _validate_where_expressions to a class-attribute lookup\n  against _BACKENDS, avoiding eager backend instantiation at chain\n  time and removing the type(backend).__name__ fragility in error\n  messages.\n- Add ModelRegistry.unregister_mapping() and use it in the new DII\n  test fixture instead of poking the private _mappings indexes.\n- Make the codegen tomli ignore portable across mypy environments\n  via unused-ignore so doit check passes whether or not tomli is\n  installed.\n\nAddresses #683.",
          "timestamp": "2026-05-05T16:53:53+01:00",
          "tree_id": "f273b741748cd1ac46ffdee9546ddd9260542d23",
          "url": "https://github.com/endavis/pynetappfoundry/commit/e7a91ed1fd62add94ade0ee3e39afe8287b60f93"
        },
        "date": 1777996831108,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1180577.137578954,
            "unit": "iter/sec",
            "range": "stddev: 2.8806384983250955e-7",
            "extra": "mean: 847.0433385240129 nsec\nrounds: 125708"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 739731.6431731152,
            "unit": "iter/sec",
            "range": "stddev: 4.2806425960436666e-7",
            "extra": "mean: 1.3518415890801305 usec\nrounds: 190877"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 471979.34448689147,
            "unit": "iter/sec",
            "range": "stddev: 5.27998467235683e-7",
            "extra": "mean: 2.118736787278566 usec\nrounds: 161265"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 468138.84640932817,
            "unit": "iter/sec",
            "range": "stddev: 5.047905802537811e-7",
            "extra": "mean: 2.136118392374613 usec\nrounds: 166058"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 507770.9507080355,
            "unit": "iter/sec",
            "range": "stddev: 5.14624253909285e-7",
            "extra": "mean: 1.969391905160389 usec\nrounds: 64189"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 163314.93304560165,
            "unit": "iter/sec",
            "range": "stddev: 8.892720497000043e-7",
            "extra": "mean: 6.123138780706445 usec\nrounds: 60347"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 140903.85242268714,
            "unit": "iter/sec",
            "range": "stddev: 9.42040917896276e-7",
            "extra": "mean: 7.097038035554722 usec\nrounds: 71144"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 74906.62939211297,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018159267176509612",
            "extra": "mean: 13.349953243327906 usec\nrounds: 38155"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 234405.4469155017,
            "unit": "iter/sec",
            "range": "stddev: 7.768791511420712e-7",
            "extra": "mean: 4.266112469478917 usec\nrounds: 51534"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31773.558611718265,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028087894417376694",
            "extra": "mean: 31.47271013046661 usec\nrounds: 2991"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 77.02961939073461,
            "unit": "iter/sec",
            "range": "stddev: 0.0014322669229969113",
            "extra": "mean: 12.982019227272511 msec\nrounds: 44"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 76.29678318011258,
            "unit": "iter/sec",
            "range": "stddev: 0.0015626029241843323",
            "extra": "mean: 13.106712476190722 msec\nrounds: 42"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 85.06272629402552,
            "unit": "iter/sec",
            "range": "stddev: 0.0014160081089313649",
            "extra": "mean: 11.75603044444434 msec\nrounds: 45"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 9.493922404916798,
            "unit": "iter/sec",
            "range": "stddev: 0.0011917837772053963",
            "extra": "mean: 105.33054277777865 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 304.7115748297007,
            "unit": "iter/sec",
            "range": "stddev: 0.00009056766963280343",
            "extra": "mean: 3.281791971830696 msec\nrounds: 213"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 79.13835921906856,
            "unit": "iter/sec",
            "range": "stddev: 0.0011414699910086005",
            "extra": "mean: 12.636097208331401 msec\nrounds: 48"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.0614676980513077,
            "unit": "iter/sec",
            "range": "stddev: 0.14975732229197875",
            "extra": "mean: 16.268707495199997 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.06605660638836859,
            "unit": "iter/sec",
            "range": "stddev: 0.14484705059874795",
            "extra": "mean: 15.138531248800007 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 423798.8255837565,
            "unit": "iter/sec",
            "range": "stddev: 5.46338256627273e-7",
            "extra": "mean: 2.3596101254470496 usec\nrounds: 12740"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 404551.0492583041,
            "unit": "iter/sec",
            "range": "stddev: 5.804909314538368e-7",
            "extra": "mean: 2.4718759272368227 usec\nrounds: 86949"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 396154.9772746027,
            "unit": "iter/sec",
            "range": "stddev: 5.297797022909343e-7",
            "extra": "mean: 2.52426463723774 usec\nrounds: 106304"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 176005.56747266502,
            "unit": "iter/sec",
            "range": "stddev: 8.044832065647201e-7",
            "extra": "mean: 5.681638452461496 usec\nrounds: 49266"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 207716.04794443204,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010087115595489236",
            "extra": "mean: 4.814264520705299 usec\nrounds: 66543"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 446086.5173742109,
            "unit": "iter/sec",
            "range": "stddev: 5.212978162910418e-7",
            "extra": "mean: 2.2417176064550834 usec\nrounds: 107205"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 451174.01318478683,
            "unit": "iter/sec",
            "range": "stddev: 5.026288729507688e-7",
            "extra": "mean: 2.2164397123431643 usec\nrounds: 98146"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35616.87704040923,
            "unit": "iter/sec",
            "range": "stddev: 0.000002408033610507973",
            "extra": "mean: 28.076577260421995 usec\nrounds: 15286"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 598011.5726029463,
            "unit": "iter/sec",
            "range": "stddev: 4.241721912925847e-7",
            "extra": "mean: 1.672208441798762 usec\nrounds: 66455"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 262306.4403898792,
            "unit": "iter/sec",
            "range": "stddev: 6.578849128466979e-7",
            "extra": "mean: 3.8123349107008195 usec\nrounds: 91075"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 390192.2601352506,
            "unit": "iter/sec",
            "range": "stddev: 5.275534906891634e-7",
            "extra": "mean: 2.562839149227036 usec\nrounds: 79981"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 240746.63902821537,
            "unit": "iter/sec",
            "range": "stddev: 7.371635542258172e-7",
            "extra": "mean: 4.153744384704787 usec\nrounds: 45412"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 209427.23212007183,
            "unit": "iter/sec",
            "range": "stddev: 7.595726038187673e-7",
            "extra": "mean: 4.774928216721432 usec\nrounds: 84797"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 54581.92387089412,
            "unit": "iter/sec",
            "range": "stddev: 0.000001782457657857886",
            "extra": "mean: 18.32108377794377 usec\nrounds: 25496"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26484.63741322381,
            "unit": "iter/sec",
            "range": "stddev: 0.00006476361601361368",
            "extra": "mean: 37.757737982121625 usec\nrounds: 15789"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 36006.07740092426,
            "unit": "iter/sec",
            "range": "stddev: 0.000002487401419313171",
            "extra": "mean: 27.77308921672013 usec\nrounds: 7734"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 338.71326112267354,
            "unit": "iter/sec",
            "range": "stddev: 0.000033562731063690956",
            "extra": "mean: 2.9523497151705103 msec\nrounds: 323"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 34.12258708368057,
            "unit": "iter/sec",
            "range": "stddev: 0.00012366264203108826",
            "extra": "mean: 29.306101484850743 msec\nrounds: 33"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 821.1285863639216,
            "unit": "iter/sec",
            "range": "stddev: 0.0011360979385529777",
            "extra": "mean: 1.2178360571127447 msec\nrounds: 928"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 6.731962322211087,
            "unit": "iter/sec",
            "range": "stddev: 0.0027798150919698754",
            "extra": "mean: 148.54509757142458 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.6640008435169232,
            "unit": "iter/sec",
            "range": "stddev: 0.1016732575459304",
            "extra": "mean: 1.5060221832000025 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 788.2223382566524,
            "unit": "iter/sec",
            "range": "stddev: 0.0011300655892295074",
            "extra": "mean: 1.268677569087608 msec\nrounds: 977"
          }
        ]
      },
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
          "id": "93281e4f672f04c29eb52f5d2204c4f50209d16a",
          "message": "fix: correct nf events get EMS field mapping (merges PR #685, addresses #108)\n\n- Default --output to ems_output.csv (matches sysadmin script behaviour)\n- Remove console/Rich table output path; always write CSV\n- Add fields=\"*\" to API query so log_message, node, message.severity are returned\n- Replace .to_dict() with direct bracket access (matches azevents.py pattern)\n- Fix severity: event[\"message\"][\"severity\"] (was top-level, doesn't exist)\n- Fix message: event[\"log_message\"] (was message.text, doesn't exist)\n- Add node column to CSV output (cluster, node, time, name, severity, message)\n- Remove output_to_file parameter from _get_cluster_events\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-05-06T11:54:05+01:00",
          "tree_id": "f2dd0a9db8b76a4bddd48507318b35ed44ddcaf7",
          "url": "https://github.com/endavis/pynetappfoundry/commit/93281e4f672f04c29eb52f5d2204c4f50209d16a"
        },
        "date": 1778065240594,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1170314.7791792287,
            "unit": "iter/sec",
            "range": "stddev: 2.6652969912800225e-7",
            "extra": "mean: 854.4709660945452 nsec\nrounds: 68644"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 737358.3425756228,
            "unit": "iter/sec",
            "range": "stddev: 5.059352497296106e-7",
            "extra": "mean: 1.3561926979858385 usec\nrounds: 194932"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 463846.42448380834,
            "unit": "iter/sec",
            "range": "stddev: 4.97143246344138e-7",
            "extra": "mean: 2.1558859726316753 usec\nrounds: 163908"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 445963.8148660615,
            "unit": "iter/sec",
            "range": "stddev: 7.074689633801723e-7",
            "extra": "mean: 2.2423343927586026 usec\nrounds: 171792"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 392407.79058830335,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013224219760186982",
            "extra": "mean: 2.5483693850746074 usec\nrounds: 86866"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 153121.84698129902,
            "unit": "iter/sec",
            "range": "stddev: 0.000002008822753859628",
            "extra": "mean: 6.530746720434553 usec\nrounds: 55267"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 129906.75549663688,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023119239748587616",
            "extra": "mean: 7.6978290788417745 usec\nrounds: 68985"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 73022.33201210886,
            "unit": "iter/sec",
            "range": "stddev: 0.000002562016959824839",
            "extra": "mean: 13.694440761412219 usec\nrounds: 45494"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 232434.593983185,
            "unit": "iter/sec",
            "range": "stddev: 7.56821540854646e-7",
            "extra": "mean: 4.302285571451308 usec\nrounds: 45999"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31626.1232760704,
            "unit": "iter/sec",
            "range": "stddev: 0.00000232906595575003",
            "extra": "mean: 31.619430281442064 usec\nrounds: 3091"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 70.53857432717679,
            "unit": "iter/sec",
            "range": "stddev: 0.0013909523346930085",
            "extra": "mean: 14.176640363636105 msec\nrounds: 44"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 65.88601268269281,
            "unit": "iter/sec",
            "range": "stddev: 0.0016283448143070028",
            "extra": "mean: 15.177728311106067 msec\nrounds: 45"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 71.57299539977281,
            "unit": "iter/sec",
            "range": "stddev: 0.0014808335621162537",
            "extra": "mean: 13.97175002128211 msec\nrounds: 47"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 9.092381321946364,
            "unit": "iter/sec",
            "range": "stddev: 0.0009796029475872925",
            "extra": "mean: 109.98218888887676 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 301.80924020858583,
            "unit": "iter/sec",
            "range": "stddev: 0.00012444627978120694",
            "extra": "mean: 3.3133511727768235 msec\nrounds: 191"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 69.79897464875626,
            "unit": "iter/sec",
            "range": "stddev: 0.00228445543684208",
            "extra": "mean: 14.3268580238065 msec\nrounds: 42"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.060803533965719365,
            "unit": "iter/sec",
            "range": "stddev: 0.187708285741466",
            "extra": "mean: 16.4464124826 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.06512676879051071,
            "unit": "iter/sec",
            "range": "stddev: 0.24171463007058616",
            "extra": "mean: 15.354669340600003 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 437226.27261253557,
            "unit": "iter/sec",
            "range": "stddev: 5.039951336937485e-7",
            "extra": "mean: 2.287145266968409 usec\nrounds: 9424"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 415004.2040166367,
            "unit": "iter/sec",
            "range": "stddev: 5.445307758631984e-7",
            "extra": "mean: 2.4096141444386716 usec\nrounds: 85602"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 406201.71003616037,
            "unit": "iter/sec",
            "range": "stddev: 5.126317922412464e-7",
            "extra": "mean: 2.461831093500269 usec\nrounds: 32219"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 180431.2244666086,
            "unit": "iter/sec",
            "range": "stddev: 8.805025900784989e-7",
            "extra": "mean: 5.542277967442739 usec\nrounds: 46340"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 212661.0580796775,
            "unit": "iter/sec",
            "range": "stddev: 7.26938965143474e-7",
            "extra": "mean: 4.702318370039008 usec\nrounds: 61573"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 462474.2896170681,
            "unit": "iter/sec",
            "range": "stddev: 5.263787008242988e-7",
            "extra": "mean: 2.162282363475831 usec\nrounds: 94697"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 471102.37827267253,
            "unit": "iter/sec",
            "range": "stddev: 4.658742306144018e-7",
            "extra": "mean: 2.1226808569011366 usec\nrounds: 86491"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 36339.99018205792,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021498955218039458",
            "extra": "mean: 27.51789406078949 usec\nrounds: 17189"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 592033.0097190929,
            "unit": "iter/sec",
            "range": "stddev: 4.318560677861309e-7",
            "extra": "mean: 1.6890950058248928 usec\nrounds: 68743"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 265551.78710055473,
            "unit": "iter/sec",
            "range": "stddev: 6.54716444871356e-7",
            "extra": "mean: 3.7657438156171645 usec\nrounds: 77979"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 387767.3570881184,
            "unit": "iter/sec",
            "range": "stddev: 5.426624635674757e-7",
            "extra": "mean: 2.5788658630508565 usec\nrounds: 74767"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 237397.88602521786,
            "unit": "iter/sec",
            "range": "stddev: 7.113381424152581e-7",
            "extra": "mean: 4.212337425337367 usec\nrounds: 57598"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 211684.01726173374,
            "unit": "iter/sec",
            "range": "stddev: 8.124706720951821e-7",
            "extra": "mean: 4.724022214504575 usec\nrounds: 78778"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 54149.48239262173,
            "unit": "iter/sec",
            "range": "stddev: 0.00000163596477898885",
            "extra": "mean: 18.46739720888371 usec\nrounds: 24652"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 27013.8678689542,
            "unit": "iter/sec",
            "range": "stddev: 0.00006262889038609557",
            "extra": "mean: 37.01802366292219 usec\nrounds: 15594"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35870.61453981317,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025149496493378436",
            "extra": "mean: 27.877972341123105 usec\nrounds: 10449"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 335.3906531036324,
            "unit": "iter/sec",
            "range": "stddev: 0.000032805303543833496",
            "extra": "mean: 2.9815977003122085 msec\nrounds: 317"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 33.34328085300183,
            "unit": "iter/sec",
            "range": "stddev: 0.00039736672155231276",
            "extra": "mean: 29.991049903236263 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 817.9326219204742,
            "unit": "iter/sec",
            "range": "stddev: 0.0011576287878844803",
            "extra": "mean: 1.2225945917795022 msec\nrounds: 1046"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 6.775054426141006,
            "unit": "iter/sec",
            "range": "stddev: 0.0025719015175991256",
            "extra": "mean: 147.6002902857252 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.6719178280360553,
            "unit": "iter/sec",
            "range": "stddev: 0.08998056943246846",
            "extra": "mean: 1.4882772242000102 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 793.6425396386068,
            "unit": "iter/sec",
            "range": "stddev: 0.0011404974492946842",
            "extra": "mean: 1.2600131042060323 msec\nrounds: 1046"
          }
        ]
      },
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
          "id": "eb2489f41d348d1cb16ffa136bde127d38761b6f",
          "message": "fix: use message.severity filter and default to wildcard (merges PR #686)\n\n- Change severity API param key from 'severity' to 'message.severity'\n  (matches ONTAP EMS API and sysadmin script pattern)\n- Default message.severity to '*' when no --severity given so debug\n  events are included, matching sysadmin get_event.py behaviour\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-05-06T12:39:25+01:00",
          "tree_id": "b3ab5f8b9686fb92b43df2461dfcfa2690f23b1a",
          "url": "https://github.com/endavis/pynetappfoundry/commit/eb2489f41d348d1cb16ffa136bde127d38761b6f"
        },
        "date": 1778067970510,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1148062.2225480562,
            "unit": "iter/sec",
            "range": "stddev: 3.2012899796540946e-7",
            "extra": "mean: 871.0329286687607 nsec\nrounds: 57731"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 741122.0038435844,
            "unit": "iter/sec",
            "range": "stddev: 4.142995360588182e-7",
            "extra": "mean: 1.3493055054550134 usec\nrounds: 194553"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 469422.8460731993,
            "unit": "iter/sec",
            "range": "stddev: 5.143173588766582e-7",
            "extra": "mean: 2.130275525286354 usec\nrounds: 168039"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 465613.9034859372,
            "unit": "iter/sec",
            "range": "stddev: 5.32292571023242e-7",
            "extra": "mean: 2.147702189546414 usec\nrounds: 158705"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 506537.66917229764,
            "unit": "iter/sec",
            "range": "stddev: 5.956070672490982e-7",
            "extra": "mean: 1.9741868391230195 usec\nrounds: 82563"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 160801.18720126478,
            "unit": "iter/sec",
            "range": "stddev: 8.471531401608033e-7",
            "extra": "mean: 6.218859558221809 usec\nrounds: 57134"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 141079.69356468908,
            "unit": "iter/sec",
            "range": "stddev: 9.205381118578251e-7",
            "extra": "mean: 7.088192316929519 usec\nrounds: 70493"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 74856.20071482948,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012811308306608686",
            "extra": "mean: 13.358946759929452 usec\nrounds: 46018"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 232851.5426128037,
            "unit": "iter/sec",
            "range": "stddev: 7.879902144601755e-7",
            "extra": "mean: 4.294581812854237 usec\nrounds: 44779"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 30762.004216388617,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027860158079863944",
            "extra": "mean: 32.507634839580604 usec\nrounds: 2922"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 48.673843731768365,
            "unit": "iter/sec",
            "range": "stddev: 0.0014577256288696692",
            "extra": "mean: 20.544915365854322 msec\nrounds: 41"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 58.33643663730936,
            "unit": "iter/sec",
            "range": "stddev: 0.002260412221199254",
            "extra": "mean: 17.141945199999498 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 51.42559522233293,
            "unit": "iter/sec",
            "range": "stddev: 0.0014306992740262074",
            "extra": "mean: 19.44556977272911 msec\nrounds: 44"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.597490512884702,
            "unit": "iter/sec",
            "range": "stddev: 0.0006445739165901279",
            "extra": "mean: 116.31300999999263 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 297.47408999023725,
            "unit": "iter/sec",
            "range": "stddev: 0.00020927951021178624",
            "extra": "mean: 3.361637311111091 msec\nrounds: 180"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 49.7882410886305,
            "unit": "iter/sec",
            "range": "stddev: 0.0018241872034398304",
            "extra": "mean: 20.08506382500741 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.05853513473957843,
            "unit": "iter/sec",
            "range": "stddev: 0.419825749290076",
            "extra": "mean: 17.083756694999998 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.06519893203246972,
            "unit": "iter/sec",
            "range": "stddev: 0.14214723544235014",
            "extra": "mean: 15.337674542000013 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 428310.2209039919,
            "unit": "iter/sec",
            "range": "stddev: 5.355928297039204e-7",
            "extra": "mean: 2.334756331262418 usec\nrounds: 11688"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 408987.16470514523,
            "unit": "iter/sec",
            "range": "stddev: 5.344000849127156e-7",
            "extra": "mean: 2.445064506415352 usec\nrounds: 81480"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 404936.09911320196,
            "unit": "iter/sec",
            "range": "stddev: 5.284214559847171e-7",
            "extra": "mean: 2.469525444113208 usec\nrounds: 96722"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 176139.2391976858,
            "unit": "iter/sec",
            "range": "stddev: 8.804486082002672e-7",
            "extra": "mean: 5.6773266681234675 usec\nrounds: 47461"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 207362.5944200358,
            "unit": "iter/sec",
            "range": "stddev: 7.695865276555122e-7",
            "extra": "mean: 4.8224705270343495 usec\nrounds: 62345"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 453153.4822589046,
            "unit": "iter/sec",
            "range": "stddev: 4.940851902412333e-7",
            "extra": "mean: 2.206757840666135 usec\nrounds: 95239"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 457463.15167888784,
            "unit": "iter/sec",
            "range": "stddev: 5.072196006326308e-7",
            "extra": "mean: 2.185968413696282 usec\nrounds: 90736"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35461.14347337909,
            "unit": "iter/sec",
            "range": "stddev: 0.000002226132153118363",
            "extra": "mean: 28.199880264738404 usec\nrounds: 16620"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 600354.7283938541,
            "unit": "iter/sec",
            "range": "stddev: 4.0087474638795017e-7",
            "extra": "mean: 1.6656818922294958 usec\nrounds: 59659"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 262324.91227791895,
            "unit": "iter/sec",
            "range": "stddev: 6.336904828671032e-7",
            "extra": "mean: 3.812066461078445 usec\nrounds: 74600"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 385891.8533159059,
            "unit": "iter/sec",
            "range": "stddev: 5.094405897724954e-7",
            "extra": "mean: 2.5913996147033496 usec\nrounds: 75330"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 233481.42839646208,
            "unit": "iter/sec",
            "range": "stddev: 7.16578105281204e-7",
            "extra": "mean: 4.282995897652101 usec\nrounds: 46318"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 206766.3630583188,
            "unit": "iter/sec",
            "range": "stddev: 7.658297010666606e-7",
            "extra": "mean: 4.836376600182054 usec\nrounds: 77018"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 53478.811420682665,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017490184180499354",
            "extra": "mean: 18.698994488371422 usec\nrounds: 24671"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26426.31250745556,
            "unit": "iter/sec",
            "range": "stddev: 0.00006741292181577673",
            "extra": "mean: 37.84107221610558 usec\nrounds: 15149"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35876.10549646126,
            "unit": "iter/sec",
            "range": "stddev: 0.000002617979495407616",
            "extra": "mean: 27.873705525217552 usec\nrounds: 9882"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 337.0531670400645,
            "unit": "iter/sec",
            "range": "stddev: 0.000027658096520499924",
            "extra": "mean: 2.9668909768206775 msec\nrounds: 302"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 32.78485816730891,
            "unit": "iter/sec",
            "range": "stddev: 0.0008932926552403143",
            "extra": "mean: 30.501885806452556 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 803.7421652370062,
            "unit": "iter/sec",
            "range": "stddev: 0.0011784387169482904",
            "extra": "mean: 1.244180090645265 msec\nrounds: 1026"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 6.603813039574536,
            "unit": "iter/sec",
            "range": "stddev: 0.0027839838644892296",
            "extra": "mean: 151.42766671426347 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.6583463787433309,
            "unit": "iter/sec",
            "range": "stddev: 0.1083410482660321",
            "extra": "mean: 1.5189572424000062 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 782.6251170663851,
            "unit": "iter/sec",
            "range": "stddev: 0.0011631381500552419",
            "extra": "mean: 1.2777509668338136 msec\nrounds: 995"
          }
        ]
      },
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
          "id": "18d724a239c52ffdc6365549765ea8611d86ae0b",
          "message": "fix: use bracket access for HA detection in azevents (merges PR #687, addresses #92)\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-05-06T14:49:48+01:00",
          "tree_id": "05418bf6db711777a53c2c325f906c84a1c327bd",
          "url": "https://github.com/endavis/pynetappfoundry/commit/18d724a239c52ffdc6365549765ea8611d86ae0b"
        },
        "date": 1778075824272,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1167812.6023508355,
            "unit": "iter/sec",
            "range": "stddev: 3.2724626655650936e-7",
            "extra": "mean: 856.3017713518209 nsec\nrounds: 51317"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 727552.0603705834,
            "unit": "iter/sec",
            "range": "stddev: 4.779685834735034e-7",
            "extra": "mean: 1.3744720886236559 usec\nrounds: 185874"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 467869.6706954972,
            "unit": "iter/sec",
            "range": "stddev: 5.95332924768674e-7",
            "extra": "mean: 2.1373473482764567 usec\nrounds: 140588"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 469771.7555948957,
            "unit": "iter/sec",
            "range": "stddev: 5.527525472639695e-7",
            "extra": "mean: 2.128693324130672 usec\nrounds: 154991"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 506551.35245954397,
            "unit": "iter/sec",
            "range": "stddev: 5.979917961620866e-7",
            "extra": "mean: 1.974133511132745 usec\nrounds: 76488"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 162142.5269087819,
            "unit": "iter/sec",
            "range": "stddev: 9.909358781724274e-7",
            "extra": "mean: 6.16741344214143 usec\nrounds: 53548"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 142722.14723765457,
            "unit": "iter/sec",
            "range": "stddev: 0.000001063751731391595",
            "extra": "mean: 7.006621042036626 usec\nrounds: 68691"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 74532.99907841354,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014798215836248033",
            "extra": "mean: 13.416875912210848 usec\nrounds: 33573"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 232255.11669721047,
            "unit": "iter/sec",
            "range": "stddev: 9.120655192419144e-7",
            "extra": "mean: 4.305610202352156 usec\nrounds: 44441"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31196.614003301067,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030265345642463555",
            "extra": "mean: 32.05476081135552 usec\nrounds: 2613"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 40.534983605856915,
            "unit": "iter/sec",
            "range": "stddev: 0.0009393228573139479",
            "extra": "mean: 24.670048216215626 msec\nrounds: 37"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 38.790745803319865,
            "unit": "iter/sec",
            "range": "stddev: 0.0006518508935297166",
            "extra": "mean: 25.779344513515802 msec\nrounds: 37"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 42.08658030256699,
            "unit": "iter/sec",
            "range": "stddev: 0.001235519356100157",
            "extra": "mean: 23.76054297618965 msec\nrounds: 42"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.007613198210224,
            "unit": "iter/sec",
            "range": "stddev: 0.001777186024602673",
            "extra": "mean: 124.88115687499857 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 172.07321953965518,
            "unit": "iter/sec",
            "range": "stddev: 0.00022391115138169397",
            "extra": "mean: 5.811479570587942 msec\nrounds: 170"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 38.49646507867347,
            "unit": "iter/sec",
            "range": "stddev: 0.0004125503474119682",
            "extra": "mean: 25.976411027774777 msec\nrounds: 36"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.05444913928853181,
            "unit": "iter/sec",
            "range": "stddev: 0.6263374366741524",
            "extra": "mean: 18.365763225400002 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.05916302940236506,
            "unit": "iter/sec",
            "range": "stddev: 0.17201551289158365",
            "extra": "mean: 16.902447526799982 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 426030.1026726853,
            "unit": "iter/sec",
            "range": "stddev: 5.380395999099634e-7",
            "extra": "mean: 2.347251975216151 usec\nrounds: 10378"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 403747.48557878565,
            "unit": "iter/sec",
            "range": "stddev: 5.461490218639779e-7",
            "extra": "mean: 2.4767956104208704 usec\nrounds: 70938"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 398140.09973922337,
            "unit": "iter/sec",
            "range": "stddev: 5.947874777433736e-7",
            "extra": "mean: 2.5116786795778347 usec\nrounds: 90819"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 176047.7052461378,
            "unit": "iter/sec",
            "range": "stddev: 8.864169793810751e-7",
            "extra": "mean: 5.680278527924398 usec\nrounds: 47690"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 201546.39947064628,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012543443141087309",
            "extra": "mean: 4.961636638642322 usec\nrounds: 62819"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 451724.84743943485,
            "unit": "iter/sec",
            "range": "stddev: 5.033266581701181e-7",
            "extra": "mean: 2.2137369809706455 usec\nrounds: 96628"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 461224.3600039596,
            "unit": "iter/sec",
            "range": "stddev: 5.631496476489229e-7",
            "extra": "mean: 2.168142203051493 usec\nrounds: 97192"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35104.79838225959,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023288288165461943",
            "extra": "mean: 28.486134263211028 usec\nrounds: 15060"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 598764.2397255469,
            "unit": "iter/sec",
            "range": "stddev: 4.499779698457273e-7",
            "extra": "mean: 1.6701064186103798 usec\nrounds: 59482"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 258391.95748637803,
            "unit": "iter/sec",
            "range": "stddev: 6.651295735410998e-7",
            "extra": "mean: 3.8700894939917716 usec\nrounds: 54663"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 387395.3394067767,
            "unit": "iter/sec",
            "range": "stddev: 6.043597871711772e-7",
            "extra": "mean: 2.581342360833025 usec\nrounds: 66944"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 238280.75311299166,
            "unit": "iter/sec",
            "range": "stddev: 7.513048117750947e-7",
            "extra": "mean: 4.196730062901071 usec\nrounds: 56202"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 207922.8583176016,
            "unit": "iter/sec",
            "range": "stddev: 8.312570056350455e-7",
            "extra": "mean: 4.809476014765546 usec\nrounds: 74212"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 53122.98290350031,
            "unit": "iter/sec",
            "range": "stddev: 0.000001940530598532643",
            "extra": "mean: 18.824244147143123 usec\nrounds: 23834"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26466.42478533343,
            "unit": "iter/sec",
            "range": "stddev: 0.00007642389912738844",
            "extra": "mean: 37.78372062380551 usec\nrounds: 14876"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35546.10973268443,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028663310396215867",
            "extra": "mean: 28.13247377899433 usec\nrounds: 8886"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 325.41838354966245,
            "unit": "iter/sec",
            "range": "stddev: 0.00006657038577034924",
            "extra": "mean: 3.0729671418436904 msec\nrounds: 282"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 29.713465044188286,
            "unit": "iter/sec",
            "range": "stddev: 0.00024707424680855126",
            "extra": "mean: 33.654775655173616 msec\nrounds: 29"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 749.2615736003845,
            "unit": "iter/sec",
            "range": "stddev: 0.0013388424517499684",
            "extra": "mean: 1.3346473851511644 msec\nrounds: 862"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 5.971104905518009,
            "unit": "iter/sec",
            "range": "stddev: 0.005061540040473783",
            "extra": "mean: 167.47319228571607 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.6167645254682489,
            "unit": "iter/sec",
            "range": "stddev: 0.10767080476382233",
            "extra": "mean: 1.6213643273999878 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 738.2369562921941,
            "unit": "iter/sec",
            "range": "stddev: 0.0012938725499887908",
            "extra": "mean: 1.3545786234036759 msec\nrounds: 940"
          }
        ]
      },
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
          "id": "de1b6aad35b5b6e0c23407987336e69412cb27ae",
          "message": "feat: add Query for RPC-style POST endpoints (merges PR #689, addresses #688)\n\n* feat: add Query for RPC-style POST endpoints\n\nAdd Query class to pynetappfoundry.query as a lightweight wrapper for\nPOST-for-data RPC endpoints (e.g. /lake/query/timeseries). Completes\nthe consistent API interface trilogy alongside QuerySet (GET) and\nMutation (POST/PATCH/DELETE resource lifecycle).\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>\n\n* refactor: simplify Query.invoke kwargs forwarding\n\nAlways forward query_params to call_endpoint instead of conditionally\nbuilding a kwargs dict. Behavior is unchanged (call_endpoint defaults\nquery_params to None) but the code path is more direct.\n\nDrop tests that pinned the previous over-specified behavior:\n- test_invoke_without_query_params_omits_kwarg (assertion no longer holds)\n- test_works_with_any_mock_client (redundant — other tests already cover\n  duck-typed clients via spec'd MagicMock)\n\nUpdate test_calls_post_on_correct_path and test_invoke_with_no_body to\ninclude query_params=None in the expected call signature.\n\n---------\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>",
          "timestamp": "2026-05-06T17:13:07+01:00",
          "tree_id": "30d3cd5da9933087206ff568994f98494e5ab1e3",
          "url": "https://github.com/endavis/pynetappfoundry/commit/de1b6aad35b5b6e0c23407987336e69412cb27ae"
        },
        "date": 1778084411922,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1081680.087263138,
            "unit": "iter/sec",
            "range": "stddev: 4.0134135793523636e-7",
            "extra": "mean: 924.4877591582512 nsec\nrounds: 57104"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 700477.6616464731,
            "unit": "iter/sec",
            "range": "stddev: 5.110585827541276e-7",
            "extra": "mean: 1.4275972736225442 usec\nrounds: 159185"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 445342.36275214516,
            "unit": "iter/sec",
            "range": "stddev: 5.540968632590304e-7",
            "extra": "mean: 2.2454634538249594 usec\nrounds: 157431"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 444649.6003311619,
            "unit": "iter/sec",
            "range": "stddev: 5.876906281365548e-7",
            "extra": "mean: 2.2489618775216025 usec\nrounds: 142593"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 482416.9913372874,
            "unit": "iter/sec",
            "range": "stddev: 7.859602921412302e-7",
            "extra": "mean: 2.0728954783038276 usec\nrounds: 78223"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 155459.87867180473,
            "unit": "iter/sec",
            "range": "stddev: 9.727877200839498e-7",
            "extra": "mean: 6.432527855699188 usec\nrounds: 49559"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 136591.67516650003,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010584032541527408",
            "extra": "mean: 7.321090386958342 usec\nrounds: 67034"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 71657.81764665898,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013758919847501813",
            "extra": "mean: 13.955211487613935 usec\nrounds: 41993"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 220743.94405835116,
            "unit": "iter/sec",
            "range": "stddev: 8.634713342587231e-7",
            "extra": "mean: 4.530135602432025 usec\nrounds: 31290"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31302.52499929102,
            "unit": "iter/sec",
            "range": "stddev: 0.000002515873707006191",
            "extra": "mean: 31.94630465186592 usec\nrounds: 2859"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 40.81105850848091,
            "unit": "iter/sec",
            "range": "stddev: 0.0008415074771727769",
            "extra": "mean: 24.503162538462238 msec\nrounds: 39"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 39.29705290693685,
            "unit": "iter/sec",
            "range": "stddev: 0.0027419473876646875",
            "extra": "mean: 25.44720089743617 msec\nrounds: 39"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 44.03165295448926,
            "unit": "iter/sec",
            "range": "stddev: 0.00048498010162212704",
            "extra": "mean: 22.710934813952846 msec\nrounds: 43"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 8.443099735506694,
            "unit": "iter/sec",
            "range": "stddev: 0.001408191027606409",
            "extra": "mean: 118.43991322222456 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 272.6739511828676,
            "unit": "iter/sec",
            "range": "stddev: 0.0003858884939962946",
            "extra": "mean: 3.667383685394115 msec\nrounds: 178"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 43.80473551596589,
            "unit": "iter/sec",
            "range": "stddev: 0.001424557980581043",
            "extra": "mean: 22.8285820750024 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.055495295426664176,
            "unit": "iter/sec",
            "range": "stddev: 0.6083077349566828",
            "extra": "mean: 18.0195454824 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.06337152997295974,
            "unit": "iter/sec",
            "range": "stddev: 0.20410778009478986",
            "extra": "mean: 15.779956715999981 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 411935.7094924794,
            "unit": "iter/sec",
            "range": "stddev: 5.954199533565129e-7",
            "extra": "mean: 2.427563274939282 usec\nrounds: 11213"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 391749.18526085746,
            "unit": "iter/sec",
            "range": "stddev: 6.418566085319771e-7",
            "extra": "mean: 2.55265368154913 usec\nrounds: 80296"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 387268.4183761507,
            "unit": "iter/sec",
            "range": "stddev: 5.689107933476054e-7",
            "extra": "mean: 2.5821883545089594 usec\nrounds: 91158"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 171713.38381179923,
            "unit": "iter/sec",
            "range": "stddev: 9.307198087082313e-7",
            "extra": "mean: 5.823657875707679 usec\nrounds: 45577"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 201059.67475746642,
            "unit": "iter/sec",
            "range": "stddev: 8.122112722393311e-7",
            "extra": "mean: 4.973647755106918 usec\nrounds: 26703"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 431096.78038054734,
            "unit": "iter/sec",
            "range": "stddev: 5.925964469896738e-7",
            "extra": "mean: 2.319664737735359 usec\nrounds: 91075"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 442784.1294052803,
            "unit": "iter/sec",
            "range": "stddev: 5.140819644773296e-7",
            "extra": "mean: 2.258436862547754 usec\nrounds: 92251"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 34259.7025587097,
            "unit": "iter/sec",
            "range": "stddev: 0.000002472214088372309",
            "extra": "mean: 29.188811499058804 usec\nrounds: 16175"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 592662.1693648284,
            "unit": "iter/sec",
            "range": "stddev: 4.23200641558809e-7",
            "extra": "mean: 1.6873018925296452 usec\nrounds: 62933"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 255840.1404244149,
            "unit": "iter/sec",
            "range": "stddev: 6.819997891866421e-7",
            "extra": "mean: 3.908690787696932 usec\nrounds: 72067"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 379304.34558418,
            "unit": "iter/sec",
            "range": "stddev: 5.786774734452267e-7",
            "extra": "mean: 2.6364053342438374 usec\nrounds: 69513"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 232630.71487519683,
            "unit": "iter/sec",
            "range": "stddev: 7.548363560253117e-7",
            "extra": "mean: 4.2986585006046445 usec\nrounds: 57432"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 204769.26635048626,
            "unit": "iter/sec",
            "range": "stddev: 9.032097107692967e-7",
            "extra": "mean: 4.883545357282204 usec\nrounds: 75787"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 53339.90274238028,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018240262915037409",
            "extra": "mean: 18.747690726579965 usec\nrounds: 23788"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 25991.58072961953,
            "unit": "iter/sec",
            "range": "stddev: 0.00007306897017448933",
            "extra": "mean: 38.4739970378338 usec\nrounds: 14854"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 35207.58814773252,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028506186344652586",
            "extra": "mean: 28.402968013712215 usec\nrounds: 9379"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 332.85767217204767,
            "unit": "iter/sec",
            "range": "stddev: 0.00006894921207417663",
            "extra": "mean: 3.0042870680268394 msec\nrounds: 294"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 30.94978575635434,
            "unit": "iter/sec",
            "range": "stddev: 0.0007700688795097238",
            "extra": "mean: 32.31040136666176 msec\nrounds: 30"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 781.199251452647,
            "unit": "iter/sec",
            "range": "stddev: 0.0012078691027573511",
            "extra": "mean: 1.280083151821371 msec\nrounds: 988"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 6.2802864853165925,
            "unit": "iter/sec",
            "range": "stddev: 0.0035066964327081034",
            "extra": "mean: 159.2284049999973 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.6409592564645822,
            "unit": "iter/sec",
            "range": "stddev: 0.09546980241478913",
            "extra": "mean: 1.560161570199989 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 747.8329521142032,
            "unit": "iter/sec",
            "range": "stddev: 0.001209560588953308",
            "extra": "mean: 1.3371970266526687 msec\nrounds: 938"
          }
        ]
      },
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
          "id": "7ab66a86f1a942da3838735ea1c4207211eef4ca",
          "message": "refactor(codegen): remove dead datamodel-code-generator call (merges PR #693, addresses #692)\n\nrefactor: remove dead datamodel-code-generator call from parse_openapi_spec\n\n`parse_openapi_spec` invoked `_parse_with_datamodel_codegen(spec_path)`\nand discarded the return value. The function ran datamodel-code-generator's\nOpenAPIParser, which internally formats every generated Pydantic model\nwith `black` — costing ~20s per call on the ONTAP spec — and produced\na dict that was never read by any caller, test, or downstream tool.\n\nThe original intent (per the docstring and call-site comment) was to\n\"cross-reference type information when our own flattening logic needs\nconfirmation.\" That cross-reference was scoped but never implemented;\nno production code path depends on the result. `test_codegen_round_trip`\nremains the canonical safety net for parser correctness — it exercises\nthe full pipeline end-to-end and asserts byte-identical output against\nthe on-disk fixtures.\n\nRemoves:\n- the call site in `parse_openapi_spec`\n- the `_parse_with_datamodel_codegen` function (~40 lines)\n- the now-unused `OpenAPIParser` import\n- the docstring reference to datamodel-code-generator\n\n`tests/unit/codegen/test_roundtrip.py` runtime drops from ~33s to ~3s\nlocally. Equivalent CI savings compound across the matrix.\n\nNote: this leaves `datamodel-code-generator` as an unused project\ndependency. Removing it from `pyproject.toml` is a separate decision\nleft to the maintainer.\n\nAddresses #692",
          "timestamp": "2026-05-07T14:04:56+01:00",
          "tree_id": "a84563ec9ed1614a39647b6bed6cc1399bfb6d7c",
          "url": "https://github.com/endavis/pynetappfoundry/commit/7ab66a86f1a942da3838735ea1c4207211eef4ca"
        },
        "date": 1778159433386,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_shallow_key",
            "value": 1196704.221033984,
            "unit": "iter/sec",
            "range": "stddev: 3.551810328679703e-7",
            "extra": "mean: 835.6283720098968 nsec\nrounds: 44558"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_two_level",
            "value": 751159.4895381808,
            "unit": "iter/sec",
            "range": "stddev: 4.805491327952266e-7",
            "extra": "mean: 1.3312752004435284 usec\nrounds: 170999"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_three_level",
            "value": 486601.1685547927,
            "unit": "iter/sec",
            "range": "stddev: 5.677404535141957e-7",
            "extra": "mean: 2.055071102623949 usec\nrounds: 163693"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_four_level",
            "value": 482109.6961355528,
            "unit": "iter/sec",
            "range": "stddev: 5.326710905830956e-7",
            "extra": "mean: 2.074216735352351 usec\nrounds: 156495"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_array_index",
            "value": 521901.14567901334,
            "unit": "iter/sec",
            "range": "stddev: 4.927938226264025e-7",
            "extra": "mean: 1.916071670429008 usec\nrounds: 72945"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard",
            "value": 162953.11945686844,
            "unit": "iter/sec",
            "range": "stddev: 0.000001149158180618219",
            "extra": "mean: 6.136734315569129 usec\nrounds: 53891"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_wildcard_nested",
            "value": 144150.086231583,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012716290702283627",
            "extra": "mean: 6.9372140256195145 usec\nrounds: 73052"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_multi_field_extraction",
            "value": 78547.49157112486,
            "unit": "iter/sec",
            "range": "stddev: 0.000001403606335473056",
            "extra": "mean: 12.731151307289025 usec\nrounds: 46508"
          },
          {
            "name": "tests/benchmarks/test_bench_dict_path.py::test_bench_filter_predicate",
            "value": 242501.18727719176,
            "unit": "iter/sec",
            "range": "stddev: 7.060165104223788e-7",
            "extra": "mean: 4.123691150662066 usec\nrounds: 42150"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_initial_capture_small",
            "value": 31632.05121820976,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019543104590192565",
            "extra": "mean: 31.61350470450445 usec\nrounds: 2657"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_no_changes",
            "value": 58.84329556701968,
            "unit": "iter/sec",
            "range": "stddev: 0.001284775011166041",
            "extra": "mean: 16.994289500000015 msec\nrounds: 40"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_some_modified",
            "value": 45.05313129636449,
            "unit": "iter/sec",
            "range": "stddev: 0.0026462389055493902",
            "extra": "mean: 22.196015487178666 msec\nrounds: 39"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_added_removed",
            "value": 64.10457129289647,
            "unit": "iter/sec",
            "range": "stddev: 0.001505687895651516",
            "extra": "mean: 15.599511545455286 msec\nrounds: 44"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_large_500_volumes",
            "value": 7.754627156944585,
            "unit": "iter/sec",
            "range": "stddev: 0.0020105391718444263",
            "extra": "mean: 128.95526500000187 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_no_changes",
            "value": 298.830829454267,
            "unit": "iter/sec",
            "range": "stddev: 0.00006076466262825649",
            "extra": "mean: 3.346374943395991 msec\nrounds: 159"
          },
          {
            "name": "tests/benchmarks/test_bench_diff.py::test_bench_diff_entity_list_100_all_modified",
            "value": 52.59703762770947,
            "unit": "iter/sec",
            "range": "stddev: 0.0022266520531266467",
            "extra": "mean: 19.01247760526297 msec\nrounds: 38"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_via_shim",
            "value": 0.07297244231863466,
            "unit": "iter/sec",
            "range": "stddev: 0.16958792835912556",
            "extra": "mean: 13.7038033568 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_lazy_metadata.py::test_bench_lazy_storage_direct_db",
            "value": 0.07480755207244241,
            "unit": "iter/sec",
            "range": "stddev: 0.18837728862766856",
            "extra": "mean: 13.367634313600002 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_simple_eq",
            "value": 404809.54216155974,
            "unit": "iter/sec",
            "range": "stddev: 4.536074718750394e-7",
            "extra": "mean: 2.470297500054728 usec\nrounds: 10800"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_numeric",
            "value": 383470.2349260538,
            "unit": "iter/sec",
            "range": "stddev: 4.740151369984672e-7",
            "extra": "mean: 2.607764329330109 usec\nrounds: 77167"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_dotted",
            "value": 384432.99702888686,
            "unit": "iter/sec",
            "range": "stddev: 5.06792717222575e-7",
            "extra": "mean: 2.6012335250318235 usec\nrounds: 92200"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_in_tuple",
            "value": 175375.35781581272,
            "unit": "iter/sec",
            "range": "stddev: 7.057982651683671e-7",
            "extra": "mean: 5.702055365442197 usec\nrounds: 43547"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_not_in",
            "value": 204942.0950554601,
            "unit": "iter/sec",
            "range": "stddev: 7.158881263559755e-7",
            "extra": "mean: 4.879427038790574 usec\nrounds: 58634"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_boolean",
            "value": 421215.729133945,
            "unit": "iter/sec",
            "range": "stddev: 4.6113888704313293e-7",
            "extra": "mean: 2.374080384073226 usec\nrounds: 95193"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filter_null",
            "value": 433233.395895522,
            "unit": "iter/sec",
            "range": "stddev: 4.812864080944158e-7",
            "extra": "mean: 2.308224641669034 usec\nrounds: 91025"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_parse_filters_batch_10",
            "value": 35276.4399469633,
            "unit": "iter/sec",
            "range": "stddev: 0.000001824716616314418",
            "extra": "mean: 28.347531709646994 usec\nrounds: 15153"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_scalar",
            "value": 591353.5967247093,
            "unit": "iter/sec",
            "range": "stddev: 4.129199451198774e-7",
            "extra": "mean: 1.6910356266346116 usec\nrounds: 59899"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_resolve_json_subfield",
            "value": 263224.0415295191,
            "unit": "iter/sec",
            "range": "stddev: 7.676077818834989e-7",
            "extra": "mean: 3.7990450803402607 usec\nrounds: 66437"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_eq",
            "value": 372915.7099895251,
            "unit": "iter/sec",
            "range": "stddev: 4.662069004811253e-7",
            "extra": "mean: 2.6815711250890693 usec\nrounds: 61638"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_in",
            "value": 233785.8542180129,
            "unit": "iter/sec",
            "range": "stddev: 6.678190190396977e-7",
            "extra": "mean: 4.277418765754183 usec\nrounds: 38869"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_build_condition_json",
            "value": 209305.87151002657,
            "unit": "iter/sec",
            "range": "stddev: 6.682940554858331e-7",
            "extra": "mean: 4.777696835667107 usec\nrounds: 66525"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_5_filters",
            "value": 53713.49126121716,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013659583892987943",
            "extra": "mean: 18.61729663292305 usec\nrounds: 21889"
          },
          {
            "name": "tests/benchmarks/test_bench_query_engine.py::test_bench_where_clause_10_filters",
            "value": 26514.879426126943,
            "unit": "iter/sec",
            "range": "stddev: 0.0000738841606059732",
            "extra": "mean: 37.71467272880113 usec\nrounds: 13472"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_single",
            "value": 36480.62867014407,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016848063818936885",
            "extra": "mean: 27.41180830631916 usec\nrounds: 8451"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_100",
            "value": 343.8706223863991,
            "unit": "iter/sec",
            "range": "stddev: 0.00003462144144396798",
            "extra": "mean: 2.908070462839144 msec\nrounds: 296"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_model_to_row_batch_1000",
            "value": 32.454766846590864,
            "unit": "iter/sec",
            "range": "stddev: 0.0002839644847070943",
            "extra": "mean: 30.812114741937904 msec\nrounds: 31"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_single",
            "value": 985.2619171585991,
            "unit": "iter/sec",
            "range": "stddev: 0.0010544377510361054",
            "extra": "mean: 1.0149585430886277 msec\nrounds: 1230"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_100",
            "value": 7.816730398207032,
            "unit": "iter/sec",
            "range": "stddev: 0.004465498519712378",
            "extra": "mean: 127.93072666666048 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_row_to_model_batch_1000",
            "value": 0.78069372181183,
            "unit": "iter/sec",
            "range": "stddev: 0.12604385741074037",
            "extra": "mean: 1.2809120555999924 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmarks/test_bench_serialization.py::test_bench_round_trip_single",
            "value": 939.8016482272874,
            "unit": "iter/sec",
            "range": "stddev: 0.0010278316276209683",
            "extra": "mean: 1.0640543160211118 msec\nrounds: 1136"
          }
        ]
      }
    ]
  }
}