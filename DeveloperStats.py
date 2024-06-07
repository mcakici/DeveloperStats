import subprocess
import locale
import pandas as pd
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

developer_aliases = {
    "Mustafa Çakıcı": ["Mustafa Çakıcı", "mustafa.cakici", "Adamium", "mcakici"],
}

def get_developers():
    try:
        result = subprocess.run(
            ['git', 'log', '--format=%aN'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            encoding='utf-8'
        )
        developers = result.stdout.splitlines()
        unique_developers = set(developers)

        return unique_developers
    except subprocess.CalledProcessError as e:
        print(f"Error executing git command: {e}")
        return None

def get_lines_of_code_by_author(author):
    try:
        result = subprocess.run(
            ['git', 'log', '--author', author, '--pretty=tformat:', '--numstat'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            encoding='utf-8'
        )

        lines = result.stdout.splitlines()
        added = 0
        removed = 0
        total = 0

        for line in lines:
            if line:
                parts = line.split()
                if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
                    additions = int(parts[0])
                    deletions = int(parts[1])
                    added += additions
                    removed += deletions
                    total += additions - deletions

        return {
            'added_lines': added,
            'removed_lines': removed,
            'total_lines': total
        }
    except subprocess.CalledProcessError as e:
        print(f"Error executing git command: {e}")
        return None

developers = get_developers()

if developers:
    sorted_developers = sorted(developers, key=locale.strxfrm)
    print("Geliştiriciler: " + " " + str(len(sorted_developers)))
    print("###########################################################")
    developer_stats = {}

    for developer in sorted_developers:
        loc_stats = get_lines_of_code_by_author(developer)
        print('=> ' + developer)
        if loc_stats:
            # Geliştirici adını eşleştir
            for real_name, aliases in developer_aliases.items():
                if developer in aliases:
                    developer = real_name
                    break

            if developer in developer_stats:
                developer_stats[developer]['added_lines'] += loc_stats['added_lines']
                developer_stats[developer]['removed_lines'] += loc_stats['removed_lines']
                developer_stats[developer]['total_lines'] += loc_stats['total_lines']
            else:
                developer_stats[developer] = loc_stats

            print(f"Added lines: {locale.format_string('%d', loc_stats['added_lines'], grouping=True)}")
            print(f"Removed lines: {locale.format_string('%d', loc_stats['removed_lines'], grouping=True)}")
            print(f"Total lines: {locale.format_string('%d', loc_stats['total_lines'], grouping=True)}")
        print("--------------------------------------------")

    sorted_by_added_lines = sorted(developer_stats.items(), key=lambda x: x[1]['added_lines'], reverse=True)
    print("###########################################################")

    # DataFrame oluştur
    df = pd.DataFrame([{
        'Developer': developer,
        'Added Lines': locale.format_string('%d', stats['added_lines'], grouping=True),
        'Removed Lines': locale.format_string('%d', stats['removed_lines'], grouping=True),
        'Total Lines': locale.format_string('%d', stats['total_lines'], grouping=True)
    } for developer, stats in sorted_by_added_lines])

    # DataFrame'i yazdır
    print(df.to_string(index=False))
else:
    print("Geliştirici adları alınamadı.")
    exit

print("###########################################################")
input("Press Enter to exit...")