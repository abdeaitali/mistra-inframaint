import cProfile
import pstats
#profiler = cProfile.Profile()
#profiler.enable()
#import analyse_optram_bis_main_v2
#profiler.disable()
#profiler.dump_stats('profile_dump')

stats = pstats.Stats('profile_dump')
stats.strip_dirs().sort_stats('cumtime').print_stats(20)


