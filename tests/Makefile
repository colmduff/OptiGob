# Define the test target
test:
	@echo "Running all Python unit tests..."
	@python -m unittest discover -s . -p "*.py"

# Define the clean target
clean:
	@echo "Cleaning up..."
	@rm -rf *.log

# Define the default target
all: test
