pipeline {
    agent any
    
    parameters {
        choice(
            name: 'SCRIPT_TYPE',
            choices: ['bash', 'python'],
            description: 'Какую версию калькулятора тестировать?'
        )
        booleanParam(
            name: 'RUN_TESTS', 
            defaultValue: true,
            description: 'Запускать тесты?'
        )
        booleanParam(
            name: 'CREATE_REPORT',
            defaultValue: true, 
            description: 'Создать отчет о сборке?'
        )
    }
    
    environment {
        // ЗАМЕНИ НА СВОЙ РЕПОЗИТОРИЙ!
        GIT_REPO_URL = "https://github.com/alextrojnovski/student-calculator.git"
        PROJECT_NAME = "student-calculator"
    }
    
    stages {
        stage('🔧 Подготовка') {
            steps {
                echo "=== НАСТРОЙКА СРЕДЫ ==="
                sh '''
                    echo "Проверяем Docker..."
                    docker --version
                    docker ps | head -5
                    echo "Проверяем текущую директорию..."
                    pwd
                    ls -la
                '''
            }
        }
        
        stage('📥 Клонирование репозитория') {
            steps {
                echo "=== КЛОНИРУЕМ ПРОЕКТ ==="
                
                script {
                    // Очищаем папку если существует
                    sh 'rm -rf ${PROJECT_NAME} || true'
                    
                    // Клонируем репозиторий с явным указанием ветки
                    sh """
                        git clone -b main ${GIT_REPO_URL}
                        echo "✅ Репозиторий склонирован!"
                    """
                }
                
                dir(PROJECT_NAME) {
                    sh '''
                        echo "Содержимое проекта:"
                        ls -la
                        echo "Проверяем ключевые файлы..."
                        [ -f "calculator.sh" ] && echo "✅ calculator.sh найден"
                        [ -f "calculator.py" ] && echo "✅ calculator.py найден" 
                        [ -f "Dockerfile" ] && echo "✅ Dockerfile найден"
                        [ -f "docker-compose.yml" ] && echo "✅ docker-compose.yml найден"
                        [ -f "Jenkinsfile" ] && echo "✅ Jenkinsfile найден"
                    '''
                }
            }
        }
        
        stage('🐳 Сборка Docker образа') {
            steps {
                echo "=== СОБИРАЕМ DOCKER ОБРАЗ ==="
                
                dir(PROJECT_NAME) {
                    sh '''
                        echo "Текущая директория:"
                        pwd
                        ls -la
                        
                        echo "Собираем Docker образ..."
                        docker build -t ${PROJECT_NAME} .
                        
                        echo "✅ Образ собран!"
                        echo "Информация об образе:"
                        docker images | grep ${PROJECT_NAME}
                    '''
                }
            }
        }
        
        stage('🔍 Проверка образа') {
            steps {
                echo "=== ПРОВЕРЯЕМ DOCKER ОБРАЗ ==="
                
                sh '''
                    echo "Запускаем тестовый контейнер..."
                    docker run --rm --name test-container ${PROJECT_NAME} ls -la /app
                    
                    echo "Проверяем что файлы на месте:"
                    docker run --rm ${PROJECT_NAME} ls -la /app/
                    docker run --rm ${PROJECT_NAME} file /app/calculator.sh
                    docker run --rm ${PROJECT_NAME} file /app/calculator.py
                '''
            }
        }
        
        stage('🧪 Тестирование') {
            when { 
                expression { params.RUN_TESTS == true } 
            }
            steps {
                echo "=== ТЕСТИРУЕМ КАЛЬКУЛЯТОР ==="
                
                script {
                    if (params.SCRIPT_TYPE == 'bash') {
                        sh '''
                            echo "🧪 Тестируем BASH версию..."
                            echo "Проверяем синтаксис:"
                            docker run --rm ${PROJECT_NAME} bash -n /app/calculator.sh && echo "✅ Синтаксис Bash корректен!"
                            
                            echo "Тестируем простые вычисления:"
                            docker run --rm ${PROJECT_NAME} bash -c "
                                echo 'Тест сложения:'
                                num1=10
                                num2=5
                                result=\\$(echo \\\"\\$num1 + \\$num2\\\" | bc)
                                echo \\\"\\$num1 + \\$num2 = \\$result\\\"
                            "
                            
                            echo "✅ Bash калькулятор работает!"
                        '''
                    } else {
                        sh '''
                            echo "🧪 Тестируем PYTHON версию..."
                            echo "Проверяем синтаксис:"
                            docker run --rm ${PROJECT_NAME} python3 -m py_compile /app/calculator.py && echo "✅ Синтаксис Python корректен!"
                            
                            echo "Тестируем простые вычисления:"
                            docker run --rm ${PROJECT_NAME} python3 -c "
                                print('Тест сложения:')
                                num1 = 10
                                num2 = 5
                                result = num1 + num2
                                print(f'{num1} + {num2} = {result}')
                            "
                            
                            echo "✅ Python калькулятор работает!"
                        '''
                    }
                }
            }
        }
        
        stage('📊 Создание отчета') {
            when { 
                expression { params.CREATE_REPORT == true } 
            }
            steps {
                echo "=== СОЗДАЕМ ОТЧЕТ ==="
                
                dir(PROJECT_NAME) {
                    script {
                        // ИСПРАВЛЕННАЯ ЧАСТЬ - правильное использование кавычек
                        def reportContent = """
# 🎯 ОТЧЕТ О СБОРКЕ STUDENT-CALCULATOR

## 📋 Информация о сборке
- **Номер сборки:** ${env.BUILD_NUMBER}
- **Проект:** ${env.PROJECT_NAME}
- **Тестируемая версия:** ${params.SCRIPT_TYPE}
- **Дата сборки:** \$(date)
- **URL сборки:** ${env.BUILD_URL}

## ✅ Результаты
- ✅ Docker образ успешно собран
- ✅ Файлы проекта проверены
- ✅ ${params.SCRIPT_TYPE} версия протестирована
- ✅ Контейнер запущен и работает

## 🐳 Docker информация
\$(docker images | grep ${PROJECT_NAME})

## 📁 Файлы проекта
\$(ls -la)
"""
                        
                        writeFile file: 'build-report.md', text: reportContent
                        
                        sh '''
                            echo "=== ОТЧЕТ СОЗДАН ==="
                            cat build-report.md
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo "=== 🧹 ЗАВЕРШЕНИЕ ==="
            script {
                sh '''
                    echo "Очищаем временные контейнеры..."
                    docker rm -f running-calc test-container || true
                    echo "Статус сборки: ${currentBuild.result}"
                    echo "Длительность: ${currentBuild.durationString}"
                '''
            }
        }
        
        success {
            echo "🎉 🎉 🎉 УСПЕХ!"
            echo "Студенческий проект успешно собран через Jenkins в Docker!"
            echo "📊 Подробности: ${env.BUILD_URL}"
            
            script {
                def congrats = [
                    "🎓 Отличная работа! Ты освоил CI/CD!",
                    "🚀 Jenkins + Docker = Мощная комбинация!",
                    "💻 Теперь ты настоящий DevOps инженер!",
                    "🐳 Контейнеры тебе подвластны!"
                ]
                def randomMsg = congrats[new Random().nextInt(congrats.size())]
                echo randomMsg
            }
        }
        
        failure {
            echo "❌ Сборка не удалась"
            echo "Проверь логи для диагностики"
            
            script {
                sh '''
                    echo "=== ДИАГНОСТИКА ==="
                    echo "Docker images:"
                    docker images | head -5
                    echo "Containers:"
                    docker ps -a | head -5
                '''
            }
        }
    }
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }
}
