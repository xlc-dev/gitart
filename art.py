import os
import subprocess
from datetime import datetime, timedelta

YEAR = 2022

# 0 = Empty
# 1 = Light Commit
# 2 = Heavy Commit

POKEBALL_SPRITE = [
    # Col 0 (Left Edge)
    [0, 2, 2, 0, 1, 1, 0],
    # Col 1
    [2, 2, 2, 0, 1, 1, 1],
    # Col 2 (Center with button hole)
    [2, 2, 0, 0, 0, 1, 1],
    # Col 3
    [2, 2, 2, 0, 1, 1, 1],
    # Col 4 (Right Edge)
    [0, 2, 2, 0, 1, 1, 0],
    # Col 5 (Spacer)
    [0, 0, 0, 0, 0, 0, 0],
]

def make_commit(date_obj, intensity):
    date_str = date_obj.strftime('%Y-%m-%d 12:00:00')
    env = os.environ.copy()
    env['GIT_COMMITTER_DATE'] = date_str
    env['GIT_AUTHOR_DATE'] = date_str
    
    # Intensity 1 = 1 commit (Light Green)
    # Intensity 2 = 5 commits (Dark Green)
    count = 1 if intensity == 1 else 5
    
    for i in range(count):
        subprocess.run(
            ['git', 'commit', '--allow-empty', '-m', f'pkm {date_str}'],
            env=env,
            stdout=subprocess.DEVNULL
        )
    print(f"Committed ({count}x): {date_str}")

def generate_art():
    # Start on the first Sunday of 2022 to align the grid
    current_date = datetime(YEAR, 1, 2)
    
    week_index = 0
    sprite_width = len(POKEBALL_SPRITE)
    
    while current_date.year == YEAR:
        sprite_col_idx = week_index % sprite_width
        column_data = POKEBALL_SPRITE[sprite_col_idx]
        
        for day_offset in range(7):
            day_date = current_date + timedelta(days=day_offset)
            
            if day_date.year != YEAR:
                break
                
            intensity = column_data[day_offset]
            
            if intensity > 0:
                make_commit(day_date, intensity)

        current_date += timedelta(weeks=1)
        week_index += 1

if __name__ == "__main__":
    generate_art()
