"""Step 1 - Prepare the Defects4J files needed by select_bugs.py."""
import csv, os, re, subprocess, sys

D4J = sys.argv[1]
REPOS = {
    'Cli': 'apache/commons-cli', 'Closure': 'google/closure-compiler',
    'Codec': 'apache/commons-codec', 'Collections': 'apache/commons-collections',
    'Compress': 'apache/commons-compress', 'Csv': 'apache/commons-csv',
    'Gson': 'google/gson', 'JacksonCore': 'FasterXML/jackson-core',
    'JacksonDatabind': 'FasterXML/jackson-databind',
    'JacksonXml': 'FasterXML/jackson-dataformat-xml', 'Jsoup': 'jhy/jsoup',
    'JxPath': 'apache/commons-jxpath', 'Lang': 'apache/commons-lang',
    'Math': 'apache/commons-math', 'Mockito': 'mockito/mockito',
    'Time': 'JodaOrg/joda-time',
}
os.makedirs('fixed', exist_ok=True); os.makedirs('buggy', exist_ok=True)
proj_dir = os.path.join(D4J, 'framework', 'projects')
jobs, failed = [], []

def fetch(repo, commit, path, out):
    # downloads with curl, which uses the system certificates;
    # older Joda-Time revisions keep the sources under JodaTime/
    for prefix in ('', 'JodaTime/'):
        url = f'https://raw.githubusercontent.com/{repo}/{commit}/{prefix}{path}'
        r = subprocess.run(['curl', '-sSfL', '--max-time', '60', '-o', out, url],
                           capture_output=True, text=True)
        if r.returncode == 0:
            return True
        last_error = r.stderr.strip()
    if os.path.exists(out):
        os.remove(out)
    print(f'  download failed: {last_error}')
    return False

for p in sorted(os.listdir(proj_dir)):
    if p not in REPOS:
        print(f'skipping {p} (not on GitHub)'); continue
    for row in csv.DictReader(open(os.path.join(proj_dir, p, 'active-bugs.csv'))):
        b = row['bug.id']
        patch = os.path.join(proj_dir, p, 'patches', f'{b}.src.patch')
        files = set(re.findall(r'^diff --git a/(\S+)', open(patch, errors='ignore').read(), re.M))
        if len(files) != 1:
            continue                       # fix spans more than one file
        path = files.pop()
        fixed, buggy = f'fixed/{p}_{b}.java', f'buggy/{p}_{b}.java'
        if not os.path.exists(fixed) and not fetch(REPOS[p], row['revision.id.fixed'], path, fixed):
            failed.append(f'{p}_{b} (download)'); continue
        # Defects4J patches go from the fixed to the faulty version
        if subprocess.run(['patch', '-s', '-o', buggy, fixed, patch]).returncode != 0:
            failed.append(f'{p}_{b} (patch)'); continue
        jobs.append(f"{p}\t{b}\t{REPOS[p]}\t{row['revision.id.fixed']}\t{path}")
        print(f'ok {p}_{b}')

open('jobs.tsv', 'w').write('\n'.join(jobs) + '\n')
print(f'\nSingle-file bugs prepared: {len(jobs)}')
if failed:
    print('Failed:', ', '.join(failed))