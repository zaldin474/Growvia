#  36 Test profiles:
# 3 per role across all 12 roles, with clear, noisy, and ambiguous cases.

EXPANDED_EVALUATION_CASES = [

    # =====================================================
    # BACKEND
    # =====================================================

    {
        "name": "backend_clear",
        "difficulty": "clear",
        "text": """
        Built RESTful services using Python and FastAPI.
        Designed PostgreSQL schemas, authentication,
        CRUD endpoints and server-side business logic.
        Used Docker and Git for development.
        """,
        "expected_roles": {
            "Backend Developer"
        }
    },

    {
        "name": "backend_aliases",
        "difficulty": "noisy",
        "text": """
        Developed APIs with NodeJS and Postgres.
        Worked with GitHub, SQL databases,
        authentication and server-side applications.
        Deployed services with Docker.
        """,
        "expected_roles": {
            "Backend Developer"
        }
    },

    {
        "name": "backend_ambiguous",
        "difficulty": "ambiguous",
        "text": """
        Built web applications using Java,
        Spring Boot, SQL and REST APIs.
        Also implemented some HTML and JavaScript
        pages for the application.
        """,
        "expected_roles": {
            "Backend Developer",
            "Full Stack Developer"
        }
    },


    # =====================================================
    # FRONTEND
    # =====================================================

    {
        "name": "frontend_clear",
        "difficulty": "clear",
        "text": """
        Created responsive interfaces using
        React, TypeScript, JavaScript,
        HTML and CSS.

        Built reusable components and
        integrated external APIs.
        """,
        "expected_roles": {
            "Frontend Developer"
        }
    },

    {
        "name": "frontend_noisy",
        "difficulty": "noisy",
        "text": """
        Worked on university web applications.
        Designed pages, forms and interactive components.
        Technologies included JS, React.js,
        HTML5, CSS3 and GitHub.
        """,
        "expected_roles": {
            "Frontend Developer"
        }
    },

    {
        "name": "frontend_ambiguous",
        "difficulty": "ambiguous",
        "text": """
        Built React and TypeScript user interfaces
        and connected them to REST APIs.

        Also wrote a small Node.js service
        and worked with SQL.
        """,
        "expected_roles": {
            "Frontend Developer",
            "Full Stack Developer"
        }
    },


    # =====================================================
    # FULL STACK
    # =====================================================

    {
        "name": "fullstack_clear",
        "difficulty": "clear",
        "text": """
        Built complete web applications with
        React, TypeScript and CSS on the client side.

        Developed REST APIs with Python,
        FastAPI and PostgreSQL on the server side.
        Used Git and Docker.
        """,
        "expected_roles": {
            "Full Stack Developer"
        }
    },

    {
        "name": "fullstack_java",
        "difficulty": "noisy",
        "text": """
        Developed a web application with
        Java Spring Boot, SQL,
        JavaScript, HTML and CSS.

        Implemented both API endpoints
        and browser-facing application pages.
        """,
        "expected_roles": {
            "Full Stack Developer"
        }
    },

    {
        "name": "fullstack_ambiguous",
        "difficulty": "ambiguous",
        "text": """
        Created REST APIs, authentication
        and database operations using NodeJS.

        Also created React pages and
        reusable UI components.
        """,
        "expected_roles": {
            "Full Stack Developer",
            "Backend Developer"
        }
    },


    # =====================================================
    # SOFTWARE ENGINEERING
    # =====================================================

    {
        "name": "software_clear",
        "difficulty": "clear",
        "text": """
        Developed Java and C++ applications
        using object-oriented programming.

        Created UML diagrams,
        applied design patterns,
        version control and software testing.
        """,
        "expected_roles": {
            "Software Engineer"
        }
    },

    {
        "name": "software_student",
        "difficulty": "noisy",
        "text": """
        Computer engineering student with projects
        in Java, C and Python.

        Worked with OOP, UML,
        design patterns, Git and SQL.
        """,
        "expected_roles": {
            "Software Engineer"
        }
    },

    {
        "name": "software_ambiguous",
        "difficulty": "ambiguous",
        "text": """
        Built Java applications and
        server-side systems using SQL.

        Used UML, Git and object-oriented design
        throughout several academic projects.
        """,
        "expected_roles": {
            "Software Engineer",
            "Backend Developer"
        }
    },


    # =====================================================
    # MACHINE LEARNING
    # =====================================================

    {
        "name": "ml_clear",
        "difficulty": "clear",
        "text": """
        Built classification systems using
        Python, PyTorch and scikit-learn.

        Performed feature engineering,
        model evaluation, NLP experiments
        and deep learning.
        """,
        "expected_roles": {
            "Machine Learning Engineer"
        }
    },

    {
        "name": "ml_transformers",
        "difficulty": "noisy",
        "text": """
        Worked with Python,
        sklearn, PyTorch and transformer models.

        Built prediction pipelines,
        trained models and evaluated
        their performance on text datasets.
        """,
        "expected_roles": {
            "Machine Learning Engineer"
        }
    },

    {
        "name": "ml_ambiguous",
        "difficulty": "ambiguous",
        "text": """
        Used Python, pandas and scikit-learn
        to explore datasets and train predictive models.

        Performed feature engineering,
        evaluation and experimentation.
        """,
        "expected_roles": {
            "Machine Learning Engineer",
            "Data Scientist"
        }
    },


    # =====================================================
    # DATA SCIENCE
    # =====================================================

    {
        "name": "datascience_clear",
        "difficulty": "clear",
        "text": """
        Used Python, pandas, NumPy
        and scikit-learn to analyze datasets.

        Performed feature engineering,
        statistical analysis,
        predictive modelling and experimentation.
        """,
        "expected_roles": {
            "Data Scientist"
        }
    },

    {
        "name": "datascience_noisy",
        "difficulty": "noisy",
        "text": """
        Explored customer data,
        cleaned datasets and created
        predictive models.

        Used Python, SQL, pandas
        and machine learning techniques.
        """,
        "expected_roles": {
            "Data Scientist"
        }
    },

    {
        "name": "datascience_ambiguous",
        "difficulty": "ambiguous",
        "text": """
        Cleaned data with pandas,
        queried information using SQL
        and trained classification models
        with scikit-learn.
        """,
        "expected_roles": {
            "Data Scientist",
            "Data Analyst"
        }
    },


    # =====================================================
    # DATA ANALYST
    # =====================================================

    {
        "name": "analyst_clear",
        "difficulty": "clear",
        "text": """
        Queried business data using SQL,
        cleaned datasets with pandas
        and produced reports from structured data.

        Focused on interpreting trends
        and presenting useful insights.
        """,
        "expected_roles": {
            "Data Analyst"
        }
    },

    {
        "name": "analyst_short",
        "difficulty": "noisy",
        "text": """
        SQL, Python, pandas and Excel.
        Data cleaning, reporting,
        business metrics and dashboards.
        """,
        "expected_roles": {
            "Data Analyst"
        }
    },

    {
        "name": "analyst_ambiguous",
        "difficulty": "ambiguous",
        "text": """
        Used SQL and Python
        to clean and explore datasets.

        Also experimented with
        simple prediction models.
        """,
        "expected_roles": {
            "Data Analyst",
            "Data Scientist"
        }
    },


    # =====================================================
    # DEVOPS
    # =====================================================

    {
        "name": "devops_clear",
        "difficulty": "clear",
        "text": """
        Managed Linux environments
        and containerized services with Docker.

        Built CI/CD pipelines,
        deployed Kubernetes workloads
        and managed infrastructure using Terraform.
        """,
        "expected_roles": {
            "DevOps Engineer"
        }
    },

    {
        "name": "devops_cloud",
        "difficulty": "noisy",
        "text": """
        Used AWS, Docker, GitHub Actions
        and Kubernetes.

        Automated deployment pipelines
        and managed cloud infrastructure.
        """,
        "expected_roles": {
            "DevOps Engineer"
        }
    },

    {
        "name": "devops_ambiguous",
        "difficulty": "ambiguous",
        "text": """
        Built Python web services
        packaged with Docker.

        Created deployment pipelines
        using GitHub Actions
        and worked with Linux servers.
        """,
        "expected_roles": {
            "DevOps Engineer",
            "Backend Developer"
        }
    },


    # =====================================================
    # MOBILE
    # =====================================================

    {
        "name": "mobile_android",
        "difficulty": "clear",
        "text": """
        Built Android applications
        using Kotlin and the Android SDK.

        Integrated REST APIs,
        local storage and mobile interfaces.
        """,
        "expected_roles": {
            "Mobile Developer"
        }
    },

    {
        "name": "mobile_crossplatform",
        "difficulty": "noisy",
        "text": """
        Created applications using Flutter
        and React Native.

        Connected applications to REST APIs
        and used GitHub for version control.
        """,
        "expected_roles": {
            "Mobile Developer"
        }
    },

    {
        "name": "mobile_ambiguous",
        "difficulty": "ambiguous",
        "text": """
        Built Java applications
        for Android devices.

        Worked with APIs,
        SQL storage and object-oriented design.
        """,
        "expected_roles": {
            "Mobile Developer",
            "Software Engineer"
        }
    },


    # =====================================================
    # CYBERSECURITY
    # =====================================================

    {
        "name": "security_clear",
        "difficulty": "clear",
        "text": """
        Performed penetration testing,
        vulnerability assessments
        and network security analysis.

        Used Nmap, Wireshark,
        Burp Suite and Linux.
        """,
        "expected_roles": {
            "Cybersecurity Engineer"
        }
    },

    {
        "name": "security_incident",
        "difficulty": "noisy",
        "text": """
        Investigated suspicious network activity,
        worked with SIEM systems,
        incident response
        and vulnerability assessment.

        Used Linux and Python.
        """,
        "expected_roles": {
            "Cybersecurity Engineer"
        }
    },

    {
        "name": "security_ambiguous",
        "difficulty": "ambiguous",
        "text": """
        Used Linux and Python
        for network analysis and automation.

        Performed security testing,
        vulnerability scanning
        and system administration.
        """,
        "expected_roles": {
            "Cybersecurity Engineer",
            "DevOps Engineer"
        }
    },


    # =====================================================
    # EMBEDDED SYSTEMS
    # =====================================================

    {
        "name": "embedded_clear",
        "difficulty": "clear",
        "text": """
        Programmed ESP32 microcontrollers
        using C and C++.

        Integrated sensors,
        controlled hardware
        and developed firmware.
        """,
        "expected_roles": {
            "Embedded Systems Engineer"
        }
    },

    {
        "name": "embedded_arduino",
        "difficulty": "noisy",
        "text": """
        Built Arduino and ESP32 projects
        involving sensors and actuators.

        Programmed low-level logic in C++
        and worked directly with hardware.
        """,
        "expected_roles": {
            "Embedded Systems Engineer"
        }
    },

    {
        "name": "embedded_ambiguous",
        "difficulty": "ambiguous",
        "text": """
        Developed C++ applications
        for hardware-connected systems.

        Used Linux, Git,
        microcontrollers and serial communication.
        """,
        "expected_roles": {
            "Embedded Systems Engineer",
            "Software Engineer"
        }
    },


    # =====================================================
    # QA
    # =====================================================

    {
        "name": "qa_clear",
        "difficulty": "clear",
        "text": """
        Created automated tests using
        Selenium and pytest.

        Performed API testing with Postman,
        regression testing
        and documented software defects.
        """,
        "expected_roles": {
            "QA Engineer"
        }
    },

    {
        "name": "qa_java",
        "difficulty": "noisy",
        "text": """
        Wrote JUnit and Selenium tests
        for Java applications.

        Created regression suites,
        tested APIs
        and tracked application defects.
        """,
        "expected_roles": {
            "QA Engineer"
        }
    },

    {
        "name": "qa_ambiguous",
        "difficulty": "ambiguous",
        "text": """
        Developed Python applications
        and wrote automated pytest suites.

        Tested REST APIs,
        reproduced bugs
        and validated application behavior.
        """,
        "expected_roles": {
            "QA Engineer",
            "Software Engineer"
        }
    }
]