from lazy_json import lazy_json
from pympler.tracker import SummaryTracker


with open("huge.json", "r") as j:
    data = lazy_json.load(j)
tracker = SummaryTracker()
print(data['001000000'])
tracker.print_diff()


from pympler import muppy, summary
all_objects = muppy.get_objects()
sum1 = summary.summarize(all_objects)
summary.print_(sum1)
strs = [ao for ao in all_objects if isinstance(ao, str)]