To initialise system from scratch:

 10. Add new generation to parameters
 20. Run robots_store_to_database
 30. Run panel_create
 40. Run panel_add_robots
 50. Run panel_play_self
 60. Run randomiser }
 70. Run variegator } overnight
 80. Run evolver    }

Then, each day:

 90. Run panel_add_networks to add a few of the best nets
         (say 3, to avoid local maxima)
 95. Run panel_play_self to reset the scores (keep all)
100. Use phpmyadmin to manually delete the worst panellists
         (Keep panel size the same (say 10, for comparability))
110. Run panel_play_self to reset the scores
120. Run panel_total_reset to clear out the database
130. Run randomiser (Don't clear out old nets as previous step did that)
140. Run variegator
150. Run evolver overnight

At any time:

200. Run PLAY_GAME to see how the nets get on against a human
