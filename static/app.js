const BASE_URL = "http://127.0.0.1:5000/api";

function generateCupcakeHTML(cupcake) {
  return `
    <div data-cupcake-id=${cupcake.id}
    <li>
    ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
    <button class="delete-button">X</button>
    </li>
    <img class="Cupcake-img"
    src="${cupcake.image}"
    alt="No Image"
    </div>
    `;
}

async function ShowInitialCupcake() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);
  console.log(response);

  for (let cupcake of response.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcake));
    $("#cupcake-list").append(newCupcake);
  }
}

$("#new-cupcake-form").on("submit", async function (evt) {
  evt.preventDefault();
  let flavor = $("#form-flavor").val();
  let size = $("#form-size").val();
  let rating = $("#form-rating").val();
  let image = $("#form-image").val();

  let response = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    size,
    rating,
    image,
  });
  let newCupcake = $(generateCupcakeHTML(response.data.cupcake));
  $("#cupcake-list").append(newCupcake);
  $("#new-cupcake-form").trigger("reset");
});

async function deleteButton(evt) {
  evt.preventDefault();
  let $cupcake = $(evt.target).closest("div");
  console.log($cupcake);
  let cupcakeId = $cupcake.attr("data-cupcake-id");
  console.log(cupcakeId);

  response = await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  console.log(response);
  $cupcake.remove();
}

$("#cupcake-list").on("click", ".delete-button", deleteButton);
$(ShowInitialCupcake);
