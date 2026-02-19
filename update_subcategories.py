import re

updates = {
    # ECS = Docker 기반 컨테이너
    "learning-aws-05.md": ["AWS", "Docker"],
    # ECS CI/CD 파이프라인
    "learning-aws-06.md": ["AWS", "Docker", "CI/CD"],
    # EKS = Kubernetes
    "learning-aws-07.md": ["AWS", "Kubernetes"],
    "learning-aws-08.md": ["AWS", "Kubernetes"],
    "learning-aws-09.md": ["AWS", "Kubernetes"],
    # EKS + 로그/모니터링
    "learning-aws-10.md": ["AWS", "Kubernetes", "Monitoring"],
    "learning-aws-11.md": ["AWS", "Kubernetes", "Monitoring"],
    # GitHub Actions 심화 (제목에 명시)
    "learning-cicd-03.md": ["CI/CD", "GitHub Actions"],
    # ArgoCD = Kubernetes GitOps
    "learning-cicd-06.md": ["CI/CD", "Kubernetes"],
    # Argo Rollouts = Kubernetes 배포
    "learning-cicd-08.md": ["CI/CD", "Kubernetes"],
    # MongoDB 제목에 명시
    "learning-database-04.md": ["Database", "MongoDB"],
    # MongoDB CRUD + Python 연동
    "learning-database-05.md": ["Database", "MongoDB", "Python"],
    # Python + DB 연동 실무
    "learning-database-06.md": ["Database", "Python"],
    # GitHub Actions + Docker 배포 자동화 (제목에 명시)
    "learning-docker-09.md": ["Docker", "CI/CD", "GitHub Actions"],
    # Linux에서 네트워크 기초 (제목에 명시)
    "learning-linux-07.md": ["Linux", "Network"],
    # 네트워크 서비스 in Linux
    "learning-linux-08.md": ["Linux", "Network"],
}

files_dir = "C:/Users/SSAFY/Desktop/Projects/prgmd_blog/files"

for fname, tags in updates.items():
    fpath = f"{files_dir}/{fname}"
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    tag_str = '["' + '", "'.join(tags) + '"]'
    new_content = re.sub(
        r'subCategory:.*',
        f'subCategory: {tag_str}',
        content,
        count=1
    )

    if new_content != content:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated: {fname} → {tag_str}")
    else:
        print(f"No change: {fname}")

print("\nDone.")
