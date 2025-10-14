document.addEventListener('DOMContentLoaded', () => {
    const userSelect = document.getElementById('user-select');
    const viewedContainer = document.getElementById('viewed-products');
    const cartContainer = document.getElementById('cart-products');
    const purchasedContainer = document.getElementById('purchased-products');
    const recommendedContainer = document.getElementById('recommended-products');

    const API_URL = 'http://127.0.0.1:5000';

    // Fetch users and populate dropdown
    fetch(`${API_URL}/users`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(users => {
            if (!users) return;
            users.forEach(user => {
                const option = document.createElement('option');
                option.value = user.user_id;
                option.textContent = user.name;
                userSelect.appendChild(option);
            });
            // Load data for the first user by default
            if (users.length > 0) {
                loadUserData(users[0].user_id);
            }
        })
        .catch(error => {
            console.error('Error fetching users:', error);
            recommendedContainer.innerHTML = '<p>Could not connect to the backend. Please ensure it is running and that there are no CORS issues.</p>';
        });

    userSelect.addEventListener('change', (e) => {
        loadUserData(e.target.value);
    });

    function loadUserData(userId) {
        if (!userId) return;
        fetchUserBehavior(userId);
        fetchRecommendations(userId);
    }

    function fetchUserBehavior(userId) {
        fetch(`${API_URL}/user_behavior?user_id=${userId}`)
            .then(response => response.json())
            .then(data => {
                updateProductList(viewedContainer, data.viewed);
                updateProductList(cartContainer, data.added_to_cart);
                updateProductList(purchasedContainer, data.purchased);
            })
            .catch(error => console.error('Error fetching user behavior:', error));
    }

    function fetchRecommendations(userId) {
        recommendedContainer.innerHTML = '<p>Loading recommendations...</p>';
        fetch(`${API_URL}/recommendations?user_id=${userId}`)
            .then(response => response.json())
            .then(data => {
                updateRecommendedList(recommendedContainer, data);
            })
            .catch(error => {
                console.error('Error fetching recommendations:', error);
                recommendedContainer.innerHTML = '<p>Could not fetch recommendations.</p>';
            });
    }

    function updateProductList(container, products) {
        container.innerHTML = '';
        if (!products || products.length === 0) {
            container.textContent = 'No products in this category.';
            return;
        }
        products.forEach(product => {
            const card = createProductCard(product);
            container.appendChild(card);
        });
    }

    function updateRecommendedList(container, recommendations) {
        container.innerHTML = '';
        if (!recommendations || recommendations.length === 0) {
            container.textContent = 'No recommendations available.';
            return;
        }
        recommendations.forEach(rec => {
            const card = createProductCard(rec.product, rec.explanation);
            container.appendChild(card);
        });
    }

    function createProductCard(product, explanation = null) {
        const card = document.createElement('div');
        card.className = 'product-card';

        let content = `
            <h4>${product.name}</h4>
            <p><strong>Category:</strong> ${product.category}</p>
            <p>${product.description}</p>
        `;

        if (explanation) {
            content += `<div class="explanation"><p><strong>Why this product?</strong> ${explanation}</p></div>`;
        }

        card.innerHTML = content;
        return card;
    }
});
