import time
from datetime import datetime
from bard import bard_trans

def summarize(paras):
  summa = []
  c = 0
  iterations_per_minute = 80
  start_time = datetime.now()
  for i, page in enumerate(paras):
    # print('\nPARA:\n',para,"\n")
    if c==0:
      summa.append(bard_trans(f"""summarize: {page}
                      just give the summary without any descriptions."""))
    else:
      summa.append(bard_trans(f"""Here is the summary of the previous page: {summa[i-1]}
                             now,
                             summarize: {page}
                      just give the summary without any descriptions."""))
    if (i + 1) % iterations_per_minute == 0:
        current_time = datetime.now()
        elapsed_time = current_time - start_time
        seconds_elapsed = elapsed_time.total_seconds()

        if seconds_elapsed < 60:
            pause_duration = 60 - seconds_elapsed
            print(f"Completed {iterations_per_minute} iterations in {seconds_elapsed} seconds. Pausing for {pause_duration} seconds...")
            time.sleep(pause_duration)

        start_time = datetime.now()
    else:
        time.sleep(1)
    # if i==50:
    #   break
    print('\n', summa[i])
  return summa