# bt-res-wrapper
Wrapper script that resolves ASLR'd instruction pointers (backtraces) printed by the wrapped process

I developed this because I had enough of staring at these while working on [scylla](https://github.com/scylladb/scylla) unit tests:
```
Reactor stalled for 4002 ms on shard 0.
Backtrace:
  0x000055d3d54d23c9
  0x000055d3d51f1932
  0x000055d3d51f6b2d
  0x00007f438278566f
  0x000055d3d731f706
  0x000055d3d72e7321
  0x000055d3d704f709
  0x000055d3d731a058
  0x000055d3d7336592
  0x000055d3d72d2c2c
  0x000055d3d72d5d30
  0x000055d3d72d564b
  0x000055d3d7040dba
  0x000055d3d71e52e1
  0x000055d3d71f0296
  0x000055d3d71e53de
  0x000055d3d71e567a
  0x000055d3d71e5ab2
  0x000055d3d71e5bb3
  0x000055d3d71e5cc4
  0x000055d3de497d2b
  0x000055d3d613f026
  0x000055d3d613f4b2
  0x000055d3d6148480
  0x000055d3d61484ff
  0x000055d3d6148596
  0x000055d3d6143938
  0x000055d3d61405bb
  0x000055d3d614ba20
  0x000055d3d55002a7
  0x000055d3d5905455
```
... and addr2line turning up with `??: ??:0` for each address because of ASLR.
Now I just run `/path/to/bt-res-wrapper.py /path/to/unit/some_scylla_test` and get nice resolved backtraces:
```
Backtrace:
seastar::backtrace_buffer::append_backtrace() at /home/botond/Workspace/scylla/seastar/core/reactor.cc:278
seastar::print_with_backtrace(seastar::backtrace_buffer&) at /home/botond/Workspace/scylla/seastar/core/reactor.cc:289
seastar::reactor::block_notifier(int) at /home/botond/Workspace/scylla/seastar/core/reactor.cc:519
?? ??:0
managed_bytes::size() const at /home/botond/Workspace/scylla/./utils/managed_bytes.hh:355
managed_bytes::operator std::experimental::fundamentals_v1::basic_string_view<signed char, std::char_traits<signed char> >() const at /home/botond/Workspace/scylla/./utils/managed_bytes.hh:330
compound_wrapper<clustering_key_prefix, clustering_key_prefix_view>::operator std::experimental::fundamentals_v1::basic_string_view<signed char, std::char_traits<signed char> >() const at /home/botond/Workspace/scylla/keys.hh:296
bound_view::tri_compare::operator()(clustering_key_prefix const&, int, clustering_key_prefix const&, int) const at /home/botond/Workspace/scylla/clustering_bounds_comparator.hh:83
int position_in_partition::tri_compare::compare<position_in_partition_view, position_in_partition_view>(position_in_partition_view const&, position_in_partition_view const&) const at /home/botond/Workspace/scylla/position_in_partition.hh:314
position_in_partition::tri_compare::operator()(position_in_partition_view const&, position_in_partition_view const&) const at /home/botond/Workspace/scylla/position_in_partition.hh:322
rows_entry::tri_compare::operator()(rows_entry const&, rows_entry const&) const at /home/botond/Workspace/scylla/mutation_partition.hh:749 (discriminator 2)
rows_entry::compare::operator()(rows_entry const&, rows_entry const&) const at /home/botond/Workspace/scylla/mutation_partition.hh:771
bool intrusive_set_external_comparator<rows_entry, &rows_entry::_link>::key_node_comparator<rows_entry::compare>::operator()<rows_entry>(boost::intrusive::compact_rbtree_node<void*>* const&, rows_entry const&) at /home/botond/Workspace/scylla/intrusive_set_external_comparator.hh:79
boost::intrusive::compact_rbtree_node<void*>* boost::intrusive::bstree_algorithms<boost::intrusive::rbtree_node_traits<void*, true> >::lower_bound_loop<rows_entry, intrusive_set_external_comparator<rows_entry, &rows_entry::_link>::key_node_comparator<rows_entry::compare> >(boost::intrusive::compact_rbtree_node<void*>*, boost::intrusive::compact_rbtree_node<void*>*, rows_entry const&, intrusive_set_external_comparator<rows_entry, &rows_entry::_link>::key_node_comparator<rows_entry::compare>) at /usr/include/boost/intrusive/bstree_algorithms.hpp:2025
boost::intrusive::compact_rbtree_node<void*>* boost::intrusive::bstree_algorithms<boost::intrusive::rbtree_node_traits<void*, true> >::lower_bound<rows_entry, intrusive_set_external_comparator<rows_entry, &rows_entry::_link>::key_node_comparator<rows_entry::compare> >(boost::intrusive::compact_rbtree_node<void*> const* const&, rows_entry const&, intrusive_set_external_comparator<rows_entry, &rows_entry::_link>::key_node_comparator<rows_entry::compare>) at /usr/include/boost/intrusive/bstree_algorithms.hpp:917
boost::intrusive::tree_iterator<boost::intrusive::mhtraits<rows_entry, intrusive_set_external_comparator_member_hook, &rows_entry::_link>, false> intrusive_set_external_comparator<rows_entry, &rows_entry::_link>::lower_bound<rows_entry, rows_entry::compare>(rows_entry const&, rows_entry::compare) at /home/botond/Workspace/scylla/intrusive_set_external_comparator.hh:195 (discriminator 4)
apply_reversibly_intrusive_set(schema const&, intrusive_set_external_comparator<rows_entry, &rows_entry::_link>&, intrusive_set_external_comparator<rows_entry, &rows_entry::_link>&) at /home/botond/Workspace/scylla/mutation_partition.cc:206 (discriminator 1)
mutation_partition::apply(schema const&, mutation_partition&&) at /home/botond/Workspace/scylla/mutation_partition.cc:357
mutation_partition::apply(schema const&, mutation_partition const&, schema const&) at /home/botond/Workspace/scylla/mutation_partition.cc:334
partition_entry::apply(schema const&, mutation_partition const&, schema const&) at /home/botond/Workspace/scylla/partition_version.cc:212
memtable::apply(mutation const&, db::rp_handle&&)::{lambda()#1}::operator()() const::{lambda()#1}::operator()() const::{lambda()#1}::operator()() const at /home/botond/Workspace/scylla/memtable.cc:480
std::result_of<memtable::apply(mutation const&, db::rp_handle&&)::{lambda()#1}::operator()() const::{lambda()#1}::operator()() const::{lambda()#1} ()>::type with_linearized_managed_bytes<memtable::apply(mutation const&, db::rp_handle&&)::{lambda()#1}::operator()() const::{lambda()#1}::operator()() const::{lambda()#1}>({lambda()#1}&&) at /home/botond/Workspace/scylla/./utils/managed_bytes.hh:417
memtable::apply(mutation const&, db::rp_handle&&)::{lambda()#1}::operator()() const::{lambda()#1}::operator()() const at /home/botond/Workspace/scylla/memtable.cc:481
_ZN8logalloc18allocating_sectionclIZZN8memtable5applyERK8mutationON2db9rp_handleEENKUlvE_clEvEUlvE_EEDcRNS_6regionEOT_ at /home/botond/Workspace/scylla/utils/logalloc.hh:656
memtable::apply(mutation const&, db::rp_handle&&)::{lambda()#1}::operator()() const at /home/botond/Workspace/scylla/memtable.cc:482
_Z14with_allocatorIZN8memtable5applyERK8mutationON2db9rp_handleEEUlvE_EDcR19allocation_strategyOT_ at /home/botond/Workspace/scylla/./utils/allocation_strategy.hh:271
memtable::apply(mutation const&, db::rp_handle&&) at /home/botond/Workspace/scylla/memtable.cc:483
make_sstable_containing(std::function<seastar::lw_shared_ptr<sstables::sstable> ()>, std::vector<mutation, std::allocator<mutation> >) at /home/botond/Workspace/scylla/tests/sstable_utils.cc:36 (discriminator 2)
create_sstable(seastar::basic_sstring<char, unsigned int, 15u> const&) at /home/botond/Workspace/scylla/tests/restricted_reader_test.cc:68 (discriminator 3)
restricted_reader_test::run_test_case()::{lambda()#1}::operator()() const at /home/botond/Workspace/scylla/tests/restricted_reader_test.cc:73 (discriminator 1)
seastar::apply_helper<restricted_reader_test::run_test_case()::{lambda()#1}, std::tuple<>&&, std::integer_sequence<unsigned long> >::apply({lambda()#1}&&, std::tuple<>) at /home/botond/Workspace/scylla/seastar/core/apply.hh:36
auto seastar::apply<restricted_reader_test::run_test_case()::{lambda()#1}>(restricted_reader_test::run_test_case()::{lambda()#1}&&, std::tuple<>&&) at /home/botond/Workspace/scylla/seastar/core/apply.hh:44
std::enable_if<!seastar::is_future<std::result_of<restricted_reader_test::run_test_case()::{lambda()#1} ()>::type>::value, seastar::future<> >::type seastar::do_void_futurize_apply_tuple<restricted_reader_test::run_test_case()::{lambda()#1}>(std::result_of&&, std::tuple<(restricted_reader_test::run_test_case()::{lambda()#1})...>&&) at /home/botond/Workspace/scylla/seastar/core/future.hh:1270
seastar::future<> seastar::futurize<void>::apply<restricted_reader_test::run_test_case()::{lambda()#1}>(restricted_reader_test::run_test_case()::{lambda()#1}&&, std::tuple<>&&) at /home/botond/Workspace/scylla/seastar/core/future.hh:1290
seastar::futurize<std::result_of<std::decay<restricted_reader_test::run_test_case()::{lambda()#1}>::type ()>::type>::type seastar::async<restricted_reader_test::run_test_case()::{lambda()#1}>(seastar::thread_attributes, std::decay&&, (std::decay<restricted_reader_test::run_test_case()::{lambda()#1}>::type&&)...)::{lambda(seastar::futurize<std::result_of<std::decay<auto:1>::type ()>::type> seastar::async<{lambda()#1}>(seastar::futurize<std::result_of<std::decay<auto:1>::type ()>::type>::type, seastar::thread_attributes, std::decay<auto:1>::type&&)::work&)#1}::operator()(seastar::futurize<std::result_of<std::decay<{lambda()#1}>::type ()>::type> seastar::async<{lambda()#1}>(seastar::futurize<std::result_of<std::decay<{lambda()#1}>::type ()>::type>::type, seastar::thread_attributes, std::decay<{lambda()#1}>::type&&)::work)::{lambda()#1}::operator()() const at /home/botond/Workspace/scylla/seastar/core/thread.hh:307
std::_Function_handler<void (), seastar::futurize<std::result_of<std::decay<restricted_reader_test::run_test_case()::{lambda()#1}>::type ()>::type>::type seastar::async<restricted_reader_test::run_test_case()::{lambda()#1}>(seastar::thread_attributes, std::decay&&, (std::decay<restricted_reader_test::run_test_case()::{lambda()#1}>::type&&)...)::{lambda(seastar::futurize<std::result_of<std::decay<auto:1>::type ()>::type> seastar::async<{lambda()#1}>(seastar::futurize<std::result_of<std::decay<auto:1>::type ()>::type>::type, seastar::thread_attributes, std::decay<auto:1>::type&&)::work&)#1}::operator()(seastar::futurize<std::result_of<std::decay<{lambda()#1}>::type ()>::type> seastar::async<{lambda()#1}>(seastar::futurize<std::result_of<std::decay<{lambda()#1}>::type ()>::type>::type, seastar::thread_attributes, std::decay<{lambda()#1}>::type&&)::work)::{lambda()#1}>::_M_invoke(std::_Any_data const&) at /usr/include/c++/6/functional:1731
std::function<void ()>::operator()() const at /usr/include/c++/6/functional:2127
seastar::thread_context::main() at /home/botond/Workspace/scylla/seastar/core/thread.cc:300
```

For now the script is quite specialized for my use-case. It's looking for a `Backtrace:` (in stderr) line to start collecting addresses. It's also not very good at interleaving stdout and stderr from the wrapped process, it may reorder lines.
