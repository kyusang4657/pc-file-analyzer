from pathlib import Path

# 사용자 입력
folder_input = input("분석할 폴더 경로를 입력하세요: ")

# 입력갑 정리
folder_input = folder_input.strip().strip('"')

# 문자열을 Path 객체로 변환
folder_path = Path(folder_input)

# 경로 검증
if not folder_path.exists():
    print("오류: 입력한 경로가 존재하지 않습니다.")

elif not folder_path.is_dir():
    print("오류: 입력한 경로가 폴더가 아닙니다.")

else:
    print("분석을 시작합니다.")
    print(f"분석 대상 폴더: {folder_path}")

    #분석 결과를 저장할 변수 준비
    file_count = 0 # 파일 개수
    folder_count = 0 # 폴더 개수
    extension_counts = {} # 딕셔너리 : 키 -> 값 형식으로 데이터를 저장
    total_size = 0 # 파일 전체 용량
    large_file = []

    print()
    print("[하위 폴더 포함 항목 목록]")

    # 하위 폴더까지 모든 항목 탐색
    for item in folder_path.rglob("*"):
        # relative_to : 현재 파일/폴더의 전체 경로에서 분석 기준 폴더 경로를 제거하고, 기준 폴더 안에서의 위치만 남기는 기능
        relative_path = item.relative_to(folder_path)
        if item.is_dir():
            print(f"[폴더] {relative_path}")
            folder_count += 1
        elif item.is_file():
            print(f"[파일] {relative_path}")
            file_count += 1

            file_size = item.stat().st_size
            total_size += file_size

            large_file.append((relative_path, file_size))

            # 파일 확장자 통계 계산
            extension = item.suffix

            if extension in extension_counts:
                extension_counts[extension] += 1
            else:
                extension_counts[extension] = 1

    # 분석 결과 출력
    total_size_mb = total_size / (1024 * 1024)
    print()
    print("[분석 결과]")
    print(f"파일 개수: {file_count}개")
    print(f"폴더 개수: {folder_count}개")
    print(f"전체 파일 용량: {total_size} bytes")
    print(f"전체 파일 용량: {total_size_mb:.2f} MB")
    print()
    print("[확장자별 파일 개수]")
    for extension, count in extension_counts.items():
        print(f"{extension}: {count}개")

    large_file.sort(key=lambda file_info: file_info[1], reverse=True)
    print()
    print("[용량이 큰 파일 TOP 10]")

    for index, file_info in enumerate(large_file[:10], start=1): # large_file 리스트를 정렬
        file_path = file_info[0]
        file_size = file_info[1]
        file_size_mb = file_size / (1024 * 1024)

        print(f"{index}. {file_path} - {file_size_mb:.2f} MB")