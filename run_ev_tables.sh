###################################
# regenerate ev & best move tables
###################################

set -e

# peek
mkdir -p tables/peeked
ev_tables_filepath="tables/peeked/ev_tables.md"
best_moves_filepath="tables/peeked/best_moves.md"
echo "\`\`\`text"  > $ev_tables_filepath
python jack.py ev_table -card 2 >> $ev_tables_filepath
python jack.py ev_table -card 3 >> $ev_tables_filepath
python jack.py ev_table -card 4 >> $ev_tables_filepath
python jack.py ev_table -card 5 >> $ev_tables_filepath
python jack.py ev_table -card 6 >> $ev_tables_filepath
python jack.py ev_table -card 7 >> $ev_tables_filepath
python jack.py ev_table -card 8 >> $ev_tables_filepath
python jack.py ev_table -card 9 >> $ev_tables_filepath
python jack.py ev_table -card F >> $ev_tables_filepath
python jack.py ev_table -card A >> $ev_tables_filepath
echo "\`\`\`"  >> $ev_tables_filepath
echo "\`\`\`text"  > $best_moves_filepath
python jack.py best_moves >> $best_moves_filepath
echo "\`\`\`"  >> $best_moves_filepath

# peek, aces split no blackjack no draw
mkdir -p tables/peeked_no_bj_no_draw
ev_tables_filepath="tables/peeked_no_bj_no_draw/ev_tables.md"
best_moves_filepath="tables/peeked_no_bj_no_draw/best_moves.md"
echo "\`\`\`text"  > $ev_tables_filepath
python jack.py ev_table --ace-no-draw --ace-no-bj -card 2 >> $ev_tables_filepath
python jack.py ev_table --ace-no-draw --ace-no-bj -card 3 >> $ev_tables_filepath
python jack.py ev_table --ace-no-draw --ace-no-bj -card 4 >> $ev_tables_filepath
python jack.py ev_table --ace-no-draw --ace-no-bj -card 5 >> $ev_tables_filepath
python jack.py ev_table --ace-no-draw --ace-no-bj -card 6 >> $ev_tables_filepath
python jack.py ev_table --ace-no-draw --ace-no-bj -card 7 >> $ev_tables_filepath
python jack.py ev_table --ace-no-draw --ace-no-bj -card 8 >> $ev_tables_filepath
python jack.py ev_table --ace-no-draw --ace-no-bj -card 9 >> $ev_tables_filepath
python jack.py ev_table --ace-no-draw --ace-no-bj -card F >> $ev_tables_filepath
python jack.py ev_table --ace-no-draw --ace-no-bj -card A >> $ev_tables_filepath
echo "\`\`\`"  >> $ev_tables_filepath
echo "\`\`\`text"  > $best_moves_filepath
python jack.py best_moves --ace-no-draw --ace-no-bj >> $best_moves_filepath
echo "\`\`\`"  >> $best_moves_filepath

# peek, hit on soft
mkdir -p tables/peeked_hit_on_soft
ev_tables_filepath="tables/peeked_hit_on_soft/ev_tables.md"
best_moves_filepath="tables/peeked_hit_on_soft/best_moves.md"
echo "\`\`\`text"  > $ev_tables_filepath
python jack.py ev_table --hos -card 2 >> $ev_tables_filepath
python jack.py ev_table --hos -card 3 >> $ev_tables_filepath
python jack.py ev_table --hos -card 4 >> $ev_tables_filepath
python jack.py ev_table --hos -card 5 >> $ev_tables_filepath
python jack.py ev_table --hos -card 6 >> $ev_tables_filepath
python jack.py ev_table --hos -card 7 >> $ev_tables_filepath
python jack.py ev_table --hos -card 8 >> $ev_tables_filepath
python jack.py ev_table --hos -card 9 >> $ev_tables_filepath
python jack.py ev_table --hos -card F >> $ev_tables_filepath
python jack.py ev_table --hos -card A >> $ev_tables_filepath
echo "\`\`\`"  >> $ev_tables_filepath
echo "\`\`\`text"  > $best_moves_filepath
python jack.py best_moves --hos >> $best_moves_filepath
echo "\`\`\`"  >> $best_moves_filepath

# peek, hit on soft, aces split no blackjack no draw
mkdir -p tables/peeked_hos_no_bj_no_draw
ev_tables_filepath="tables/peeked_hos_no_bj_no_draw/ev_tables.md"
best_moves_filepath="tables/peeked_hos_no_bj_no_draw/best_moves.md"
echo "\`\`\`text"  > $ev_tables_filepath
python jack.py ev_table --hos --ace-no-draw --ace-no-bj -card 2 >> $ev_tables_filepath
python jack.py ev_table --hos --ace-no-draw --ace-no-bj -card 3 >> $ev_tables_filepath
python jack.py ev_table --hos --ace-no-draw --ace-no-bj -card 4 >> $ev_tables_filepath
python jack.py ev_table --hos --ace-no-draw --ace-no-bj -card 5 >> $ev_tables_filepath
python jack.py ev_table --hos --ace-no-draw --ace-no-bj -card 6 >> $ev_tables_filepath
python jack.py ev_table --hos --ace-no-draw --ace-no-bj -card 7 >> $ev_tables_filepath
python jack.py ev_table --hos --ace-no-draw --ace-no-bj -card 8 >> $ev_tables_filepath
python jack.py ev_table --hos --ace-no-draw --ace-no-bj -card 9 >> $ev_tables_filepath
python jack.py ev_table --hos --ace-no-draw --ace-no-bj -card F >> $ev_tables_filepath
python jack.py ev_table --hos --ace-no-draw --ace-no-bj -card A >> $ev_tables_filepath
echo "\`\`\`"  >> $ev_tables_filepath
echo "\`\`\`text"  > $best_moves_filepath
python jack.py best_moves --hos --ace-no-draw --ace-no-bj >> $best_moves_filepath
echo "\`\`\`"  >> $best_moves_filepath

# no peek
mkdir -p tables/no_peek
ev_tables_filepath="tables/no_peek/ev_tables.md"
best_moves_filepath="tables/no_peek/best_moves.md"
echo "\`\`\`text"  > $ev_tables_filepath
python jack.py ev_table --no-peek -card 2 >> $ev_tables_filepath
python jack.py ev_table --no-peek -card 3 >> $ev_tables_filepath
python jack.py ev_table --no-peek -card 4 >> $ev_tables_filepath
python jack.py ev_table --no-peek -card 5 >> $ev_tables_filepath
python jack.py ev_table --no-peek -card 6 >> $ev_tables_filepath
python jack.py ev_table --no-peek -card 7 >> $ev_tables_filepath
python jack.py ev_table --no-peek -card 8 >> $ev_tables_filepath
python jack.py ev_table --no-peek -card 9 >> $ev_tables_filepath
python jack.py ev_table --no-peek -card F >> $ev_tables_filepath
python jack.py ev_table --no-peek -card A >> $ev_tables_filepath
echo "\`\`\`"  >> $ev_tables_filepath
echo "\`\`\`text"  > $best_moves_filepath
python jack.py best_moves --no-peek >> $best_moves_filepath
echo "\`\`\`"  >> $best_moves_filepath

# no peek, aces split no blackjack no draw
mkdir -p tables/no_peek_no_bj_no_draw
ev_tables_filepath="tables/no_peek_no_bj_no_draw/ev_tables.md"
best_moves_filepath="tables/no_peek_no_bj_no_draw/best_moves.md"
echo "\`\`\`text"  > $ev_tables_filepath
python jack.py ev_table --no-peek --ace-no-draw --ace-no-bj -card 2 >> $ev_tables_filepath
python jack.py ev_table --no-peek --ace-no-draw --ace-no-bj -card 3 >> $ev_tables_filepath
python jack.py ev_table --no-peek --ace-no-draw --ace-no-bj -card 4 >> $ev_tables_filepath
python jack.py ev_table --no-peek --ace-no-draw --ace-no-bj -card 5 >> $ev_tables_filepath
python jack.py ev_table --no-peek --ace-no-draw --ace-no-bj -card 6 >> $ev_tables_filepath
python jack.py ev_table --no-peek --ace-no-draw --ace-no-bj -card 7 >> $ev_tables_filepath
python jack.py ev_table --no-peek --ace-no-draw --ace-no-bj -card 8 >> $ev_tables_filepath
python jack.py ev_table --no-peek --ace-no-draw --ace-no-bj -card 9 >> $ev_tables_filepath
python jack.py ev_table --no-peek --ace-no-draw --ace-no-bj -card F >> $ev_tables_filepath
python jack.py ev_table --no-peek --ace-no-draw --ace-no-bj -card A >> $ev_tables_filepath
echo "\`\`\`"  >> $ev_tables_filepath
echo "\`\`\`text"  > $best_moves_filepath
python jack.py best_moves --no-peek --ace-no-draw --ace-no-bj >> $best_moves_filepath
echo "\`\`\`"  >> $best_moves_filepath

# no peek, hit on soft
mkdir -p tables/no_peek_hos
ev_tables_filepath="tables/no_peek_hos/ev_tables.md"
best_moves_filepath="tables/no_peek_hos/best_moves.md"
echo "\`\`\`text"  > $ev_tables_filepath
python jack.py ev_table --no-peek --hos -card 2 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos -card 3 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos -card 4 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos -card 5 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos -card 6 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos -card 7 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos -card 8 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos -card 9 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos -card F >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos -card A >> $ev_tables_filepath
echo "\`\`\`"  >> $ev_tables_filepath
echo "\`\`\`text"  > $best_moves_filepath
python jack.py best_moves --no-peek --hos >> $best_moves_filepath
echo "\`\`\`"  >> $best_moves_filepath

# no peek, hit on soft, aces split no blackjack no draw
mkdir -p tables/no_peek_hos_no_bj_no_draw
ev_tables_filepath="tables/no_peek_hos_no_bj_no_draw/ev_tables.md"
best_moves_filepath="tables/no_peek_hos_no_bj_no_draw/best_moves.md"
echo "\`\`\`text"  > $ev_tables_filepath
python jack.py ev_table --no-peek --hos --ace-no-draw --ace-no-bj -card 2 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos --ace-no-draw --ace-no-bj -card 3 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos --ace-no-draw --ace-no-bj -card 4 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos --ace-no-draw --ace-no-bj -card 5 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos --ace-no-draw --ace-no-bj -card 6 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos --ace-no-draw --ace-no-bj -card 7 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos --ace-no-draw --ace-no-bj -card 8 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos --ace-no-draw --ace-no-bj -card 9 >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos --ace-no-draw --ace-no-bj -card F >> $ev_tables_filepath
python jack.py ev_table --no-peek --hos --ace-no-draw --ace-no-bj -card A >> $ev_tables_filepath
echo "\`\`\`"  >> $ev_tables_filepath
echo "\`\`\`text"  > $best_moves_filepath
python jack.py best_moves --no-peek --hos --ace-no-draw --ace-no-bj >> $best_moves_filepath
echo "\`\`\`"  >> $best_moves_filepath
